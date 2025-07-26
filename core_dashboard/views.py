# core_dashboard/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import json
from decimal import Decimal
import datetime
from django.contrib.auth.decorators import login_required

from .models import TbFintechRegister, TbFintechBorrowerBio, TbFintechBorrowerLoan

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        # Format tanggal/waktu sesuai ISO 8601, pastikan timezone aware jika USE_TZ=True
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        return super().default(obj)

@login_required(login_url='/login/')
def index(request):
    """
    Renders the main dashboard page.
    Requires user to be logged in.
    """
    return render(request, 'index.html')

@login_required(login_url='/login/')
def user_list_api(request):
    """
    API endpoint to retrieve a paginated list of users with filtering options.
    """
    register_code_filter = request.GET.get('register_code')
    activation_status_filter = request.GET.get('activation_status')
    bio_fullname_filter = request.GET.get('bio_fullname')

    users_queryset = TbFintechRegister.objects.all().order_by('register_code')

    if register_code_filter:
        users_queryset = users_queryset.filter(register_code=register_code_filter)
    if activation_status_filter:
        users_queryset = users_queryset.filter(register_activation_status=activation_status_filter)
    if bio_fullname_filter:
        # Menggunakan __icontains untuk pencarian nama yang tidak case-sensitive
        # dan mencari sebagian nama.
        # Pastikan relasi tbfintechborrowerbio ada dan benar di model TbFintechRegister
        users_queryset = users_queryset.filter(
            Q(tbfintechborrowerbio__bio_fullname__icontains=bio_fullname_filter)
        )

    # Optimasi query untuk menghindari N+1 problem saat mengakses TbFintechBorrowerBio
    users_queryset = users_queryset.select_related('tbfintechborrowerbio')

    limit = request.GET.get('limit', 10)
    try:
        limit = int(limit)
        if limit <= 0: # Pastikan limit tidak nol atau negatif
            limit = 10
    except ValueError:
        limit = 10 # Default jika input tidak valid

    paginator = Paginator(users_queryset, limit)
    page = request.GET.get('page', 1)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        # Jika halaman yang diminta melebihi jumlah halaman, kembali ke halaman terakhir
        users = paginator.page(paginator.num_pages)

    data = []
    for user in users:
        full_name = 'N/A'
        try:
            # Mengakses relasi OneToOneField. Jika tidak ada, DoesNotExist akan terpicu.
            full_name = user.tbfintechborrowerbio.bio_fullname or 'N/A'
        except TbFintechBorrowerBio.DoesNotExist:
            # Jika TbFintechBorrowerBio tidak ada untuk user ini
            pass

        data.append({
            'register_code': user.register_code,
            'register_email': user.register_email,
            'bio_fullname': full_name,
            'register_activation_status': user.register_activation_status,
        })

    pagination_info = {
        'total_records': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': users.number,
        'limit': limit,
    }

    return JsonResponse({
        "status": "success",
        "data": data,
        "pagination": pagination_info
    }, encoder=CustomJSONEncoder)


@login_required(login_url='/login/')
def user_detail_api(request, register_code_param):
    """
    API endpoint to retrieve details of a specific user.
    """
    try:
        # Select related untuk mengoptimalkan query jika mengakses bio atau relasi lain
        user = TbFintechRegister.objects.select_related('tbfintechborrowerbio').get(register_code=register_code_param)
        user_data = {
            'register_code': user.register_code,
            'register_email': user.register_email,
            'register_activation_status': user.register_activation_status,
        }
        try:
            # Karena sudah select_related di atas, akses langsung tbfintechborrowerbio
            bio = user.tbfintechborrowerbio
            user_data['bio_nik'] = bio.bio_nik
            user_data['bio_fullname'] = bio.bio_fullname
            user_data['bio_occupation'] = bio.bio_occupation # Contoh detail bio lainnya
            user_data['bio_phone'] = bio.bio_phone # Contoh detail bio lainnya
            user_data['bio_mother_name'] = bio.bio_mother_name # Contoh detail bio lainnya
            user_data['bio_marriage_status'] = bio.bio_marriage_status # Contoh detail bio lainnya
            user_data['bio_last_education'] = bio.bio_last_education # Contoh detail bio lainnya
            user_data['bio_birth_date'] = bio.bio_birth_date # Contoh detail bio lainnya
            user_data['bio_place_birth_date'] = bio.bio_place_birth_date # Contoh detail bio lainnya
            user_data['bio_gender'] = bio.bio_gender # Contoh detail bio lainnya
            # Tambahkan detail bio lainnya sesuai model Anda
        except TbFintechBorrowerBio.DoesNotExist:
            user_data['bio_nik'] = 'N/A'
            user_data['bio_fullname'] = 'N/A'
            user_data['bio_occupation'] = 'N/A'
            user_data['bio_phone'] = 'N/A'
            user_data['bio_mother_name'] = 'N/A'
            user_data['bio_marriage_status'] = 'N/A'
            user_data['bio_last_education'] = 'N/A'
            user_data['bio_birth_date'] = 'N/A'
            user_data['bio_place_birth_date'] = 'N/A'
            user_data['bio_gender'] = 'N/A'
            # Tambahkan default untuk bio lainnya

        # Mengambil semua pinjaman terkait pengguna
        # Gunakan values() jika Anda hanya perlu data mentah, atau serialisasi objek jika lebih kompleks
        # Pastikan field yang diambil valid dari model TbFintechBorrowerLoan
        loans = user.tbfintechborrowerloan_set.all().values(
            'id_borrower_loan', 'loan_amount', 'loan_status', 'loan_date',
            'time_approval', 'loan_tenor', 'loan_type'
        )
        user_data['loans'] = list(loans)

        return JsonResponse({"status": "success", "data": user_data}, encoder=CustomJSONEncoder)
    except TbFintechRegister.DoesNotExist:
        return JsonResponse({"status": "error", "message": f"Pengguna dengan register_code '{register_code_param}' tidak ditemukan."}, status=404)
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"Terjadi kesalahan server: {str(e)}"}, status=500)

@login_required(login_url='/login/')
def loan_list_api(request):
    """
    API endpoint to retrieve a paginated list of loans with filtering options,
    including details from TbFintechRegister and TbFintechBorrowerBio.
    """
    loan_status_filter = request.GET.get('loan_status')
    register_code_filter = request.GET.get('register_code')
    min_amount_filter = request.GET.get('min_amount')
    max_amount_filter = request.GET.get('max_amount')

    # Dimulai dari TbFintechBorrowerLoan karena ini adalah tabel sentral untuk pinjaman
    loans_queryset = TbFintechBorrowerLoan.objects.all()

    # Apply filters
    if loan_status_filter:
        loans_queryset = loans_queryset.filter(loan_status=loan_status_filter)
    if register_code_filter:
        loans_queryset = loans_queryset.filter(register_code__register_code=register_code_filter)
    if min_amount_filter:
        try:
            min_amount_filter = Decimal(min_amount_filter)
            loans_queryset = loans_queryset.filter(loan_amount__gte=min_amount_filter)
        except (ValueError, TypeError):
            pass
    if max_amount_filter:
        try:
            max_amount_filter = Decimal(max_amount_filter)
            loans_queryset = loans_queryset.filter(loan_amount__lte=max_amount_filter)
        except (ValueError, TypeError):
            pass

    # Optimasi query: join dengan register_code dan bio_fullname
    # order_by harus dilakukan setelah filter dan join agar konsisten
    loans_queryset = loans_queryset.select_related(
        'register_code', 'register_code__tbfintechborrowerbio'
    ).order_by('-loan_date') # Urutkan berdasarkan tanggal pinjaman terbaru

    limit = request.GET.get('limit', 10)
    try:
        limit = int(limit)
        if limit <= 0:
            limit = 10
    except ValueError:
        limit = 10

    paginator = Paginator(loans_queryset, limit)
    page = request.GET.get('page', 1)

    try:
        loans = paginator.page(page)
    except PageNotAnInteger:
        loans = paginator.page(1)
    except EmptyPage:
        loans = paginator.page(paginator.num_pages)

    data = []
    for loan in loans:
        register = loan.register_code # Ini adalah instance TbFintechRegister
        borrower_bio = register.tbfintechborrowerbio if hasattr(register, 'tbfintechborrowerbio') else None

        data.append({
            'register_code': register.register_code if register else 'N/A',
            'bio_fullname': borrower_bio.bio_fullname if borrower_bio else 'N/A',
            'register_date': register.register_date if register else 'N/A',
            'register_email': register.register_email if register else 'N/A',
            'virtual_account': register.virtual_account if register else 'N/A',
            'id_borrower_loan': loan.id_borrower_loan,
            'tanggal_pengajuan': loan.loan_date, # Sesuai dengan alias 'tanggal_pengajuan'
            'loan_type': loan.loan_type,
            'loan_amount': loan.loan_amount,
            'loan_tenor': loan.loan_tenor,
            'loan_rate': loan.loan_rate,
            'loan_flat_rate': loan.loan_flat_rate,
            'fee_pg': loan.fee_pg,
            'loan_start_date': loan.loan_start_date,
            'loan_status': loan.loan_status,
        })

    pagination_info = {
        'total_records': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': loans.number,
        'limit': limit,
    }

    return JsonResponse({
        "status": "success",
        "data": data,
        "pagination": pagination_info
    }, encoder=CustomJSONEncoder)