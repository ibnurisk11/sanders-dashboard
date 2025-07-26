from django.db import models

# Model untuk tb_fintech_register
class TbFintechRegister(models.Model):
    register_code = models.CharField(primary_key=True, max_length=200) # varchar -> CharField
    register_email = models.CharField(max_length=200)
    register_password = models.TextField() # text -> TextField (bisa juga CharField jika ada batasan length)
    register_how_know_sanders = models.CharField(max_length=200, blank=True, null=True)
    register_date = models.DateTimeField(blank=True, null=True)
    register_last_signin = models.DateTimeField(blank=True, null=True)
    register_last_signout = models.DateTimeField(blank=True, null=True)
    register_activation_code = models.CharField(max_length=200, blank=True, null=True)
    register_activation_status = models.CharField(max_length=50, blank=True, null=True) # enum -> CharField
    register_status = models.CharField(max_length=50, blank=True, null=True) # varchar -> CharField
    register_access_status = models.CharField(max_length=50, blank=True, null=True) # enum -> CharField
    term_status = models.CharField(max_length=50, blank=True, null=True) # enum -> CharField
    reference_code = models.CharField(max_length=200, blank=True, null=True)
    register_date_password = models.DateTimeField(blank=True, null=True)
    virtual_account = models.CharField(max_length=200, blank=True, null=True)
    va_bni = models.CharField(max_length=200, blank=True, null=True)
    va_alfamart = models.CharField(max_length=200, blank=True, null=True)
    va_mandiri = models.CharField(max_length=200, blank=True, null=True)
    expired_date_va_mandiri = models.DateTimeField(blank=True, null=True)
    cif_number_rdl = models.CharField(max_length=200, blank=True, null=True)
    account_number_rdl = models.CharField(max_length=200, blank=True, null=True)
    status_rdl_lender = models.CharField(max_length=50, blank=True, null=True) # enum -> CharField
    status_digisign = models.CharField(max_length=50, blank=True, null=True) # enum -> CharField
    status_ttd = models.CharField(max_length=50, blank=True, null=True) # enum -> CharField
    register_hcp = models.CharField(max_length=50, blank=True, null=True) # enum -> CharField
    android_phone_id = models.CharField(max_length=200, blank=True, null=True)
    ios_phone_id = models.CharField(max_length=200, blank=True, null=True)
    is_sme = models.BooleanField(blank=True, null=True) # tinyint(1) -> BooleanField
    id_marketing = models.IntegerField(blank=True, null=True) # int -> IntegerField
    full_registration_date = models.DateTimeField(blank=True, null=True) # timestamp -> DateTimeField
    is_send_nda = models.BooleanField(blank=True, null=True) # tinyint(1) -> BooleanField
    send_nda_date = models.DateTimeField(blank=True, null=True)
    digisign_registration_date = models.DateTimeField(blank=True, null=True)
    is_send_letter = models.BooleanField(blank=True, null=True) # tinyint(1) -> BooleanField
    send_letter_date = models.DateTimeField(blank=True, null=True)
    is_ttd_letter = models.BooleanField(blank=True, null=True) # tinyint(1) -> BooleanField
    click_subject_code = models.CharField(max_length=200, blank=True, null=True)
    status_rdl_proses = models.CharField(max_length=50, blank=True, null=True) # enum -> CharField
    is_read_guide_crowdfunding = models.IntegerField(blank=True, null=True) # int -> IntegerField


    class Meta:
        managed = False
        db_table = 'tb_fintech_register'

    def __str__(self):
        return self.register_code

# Model untuk tb_fintech_borrower_bio
class TbFintechBorrowerBio(models.Model):
    # Menggunakan OneToOneField karena register_code kemungkinan unik di bio (primary key).
    # db_column='register_code' diperlukan karena nama kolom di DB beda dengan nama field Django.
    register_code = models.OneToOneField(TbFintechRegister, models.DO_NOTHING, db_column='register_code', primary_key=True)
    id_borrower_bio = models.IntegerField(blank=True, null=True) # id_borrower_bio bukan PK di sini, PKnya register_code
    bio_fullname = models.CharField(max_length=200, blank=True, null=True)
    bio_place_birth_date = models.CharField(max_length=200, blank=True, null=True)
    bio_birth_date = models.DateField(blank=True, null=True)
    bio_gender = models.CharField(max_length=50, blank=True, null=True)
    bio_phone = models.CharField(max_length=50, blank=True, null=True)
    bio_marriage_status = models.CharField(max_length=50, blank=True, null=True)
    bio_spouse_name = models.CharField(max_length=200, blank=True, null=True)
    bio_spouse_phone = models.CharField(max_length=50, blank=True, null=True)
    bio_spouse_nik = models.CharField(max_length=200, blank=True, null=True)
    bio_spouse_birthday = models.DateField(blank=True, null=True)
    bio_spouse_well = models.CharField(max_length=50, blank=True, null=True) # enum -> CharField
    bio_occupation = models.TextField(blank=True, null=True)
    bio_occupation_government = models.TextField(blank=True, null=True)
    bio_country = models.CharField(max_length=100, blank=True, null=True)
    bio_province = models.CharField(max_length=100, blank=True, null=True)
    bio_city = models.CharField(max_length=100, blank=True, null=True)
    bio_district = models.CharField(max_length=100, blank=True, null=True)
    bio_village = models.CharField(max_length=100, blank=True, null=True)
    bio_rw_address = models.CharField(max_length=10, blank=True, null=True)
    bio_rt_address = models.CharField(max_length=10, blank=True, null=True)
    bio_address = models.TextField(blank=True, null=True)
    bio_post_code = models.IntegerField(blank=True, null=True) # int -> IntegerField
    bio_reference_code = models.CharField(max_length=200, blank=True, null=True)
    bio_mother_name = models.CharField(max_length=200, blank=True, null=True)
    bio_parent_name = models.CharField(max_length=200, blank=True, null=True)
    bio_parent_status = models.CharField(max_length=50, blank=True, null=True)
    bio_parent_phone = models.CharField(max_length=50, blank=True, null=True)
    bio_parent_province = models.CharField(max_length=100, blank=True, null=True)
    bio_parent_city = models.CharField(max_length=100, blank=True, null=True)
    bio_parent_district = models.CharField(max_length=100, blank=True, null=True)
    bio_parent_village = models.CharField(max_length=100, blank=True, null=True)
    bio_parent_rw_address = models.CharField(max_length=10, blank=True, null=True)
    bio_parent_rt_address = models.CharField(max_length=10, blank=True, null=True)
    bio_last_education = models.TextField(blank=True, null=True)
    bio_parent_address = models.TextField(blank=True, null=True)
    bio_parent_post_code = models.CharField(max_length=20, blank=True, null=True)
    bio_cityzenship = models.TextField(blank=True, null=True)
    bio_nik = models.CharField(max_length=200, blank=True, null=True)
    bio_upload_nik = models.TextField(blank=True, null=True) # URL atau path file
    bio_passport = models.CharField(max_length=200, blank=True, null=True)
    bio_upload_passport = models.TextField(blank=True, null=True) # URL atau path file
    bio_other_phone = models.CharField(max_length=50, blank=True, null=True)
    bio_other_name = models.CharField(max_length=200, blank=True, null=True)
    bio_other_relation = models.CharField(max_length=100, blank=True, null=True)
    bio_other_province = models.CharField(max_length=100, blank=True, null=True)
    bio_other_city = models.CharField(max_length=100, blank=True, null=True)
    bio_other_district = models.CharField(max_length=100, blank=True, null=True)
    bio_other_village = models.CharField(max_length=100, blank=True, null=True)
    bio_other_rw_address = models.CharField(max_length=10, blank=True, null=True)
    bio_other_rt_address = models.CharField(max_length=10, blank=True, null=True)
    bio_other_address = models.TextField(blank=True, null=True)
    bio_other_post_code = models.CharField(max_length=20, blank=True, null=True)
    bio_upload_selfie = models.TextField(blank=True, null=True) # URL atau path file
    bio_upload_ttd = models.TextField(blank=True, null=True) # URL atau path file
    bio_date_update = models.DateField(blank=True, null=True)
    bio_religion_name = models.CharField(max_length=100, blank=True, null=True)
    bio_position = models.CharField(max_length=100, blank=True, null=True)
    bio_spouse_place_birth_date = models.CharField(max_length=200, blank=True, null=True)
    bio_npwp = models.CharField(max_length=50, blank=True, null=True)
    bio_npwp_status = models.IntegerField(blank=True, null=True) # int -> IntegerField
    borrower_pic_length_of_work = models.DateField(blank=True, null=True)
    bio_province_domicile = models.CharField(max_length=100, blank=True, null=True)
    bio_city_domicile = models.CharField(max_length=100, blank=True, null=True)
    bio_district_domicile = models.CharField(max_length=100, blank=True, null=True)
    bio_village_domicile = models.CharField(max_length=100, blank=True, null=True)
    bio_rw_address_domicile = models.CharField(max_length=10, blank=True, null=True)
    bio_rt_address_domicile = models.CharField(max_length=10, blank=True, null=True)
    bio_address_domicile = models.TextField(blank=True, null=True)
    bio_post_code_domicile = models.CharField(max_length=20, blank=True, null=True)
    borrower_montly_income = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True) # decimal -> DecimalField
    borrower_industry_type = models.CharField(max_length=200, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'tb_fintech_borrower_bio'

    def __str__(self):
        return self.bio_fullname or f"Bio for {self.register_code.register_code}"

# Model untuk tb_fintech_borrower_loan (diganti dari tb_fintech_loan_transactions)
class TbFintechBorrowerLoan(models.Model):
    id_borrower_loan = models.CharField(primary_key=True, max_length=255) # varchar -> CharField
    register_code = models.ForeignKey(TbFintechRegister, models.DO_NOTHING, db_column='register_code') # Foreign Key
    loan_date = models.DateTimeField(blank=True, null=True)
    time_approval = models.DateTimeField(blank=True, null=True)
    loan_type = models.CharField(max_length=50, blank=True, null=True)
    loan_needs = models.CharField(max_length=255, blank=True, null=True)
    loan_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    loan_tenor = models.IntegerField(blank=True, null=True)
    loan_rating = models.CharField(max_length=10, blank=True, null=True) # enum -> CharField
    loan_rate = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True) # Sesuaikan max_digits/decimal_places
    loan_flat_rate = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    loan_principal = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    loan_interest = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    loan_montly = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    loan_note = models.TextField(blank=True, null=True)
    loan_status = models.CharField(max_length=50, blank=True, null=True)
    loan_payment = models.CharField(max_length=50, blank=True, null=True)
    amount_left = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    time_left = models.TimeField(blank=True, null=True)
    payment_estimate = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    payment_realization = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    completion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True) # Mungkin persentase?
    loan_start_date = models.DateField(blank=True, null=True)
    insurance_rate = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    commision_lender = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    commision_borrower = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    penalty = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    fee_pg = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    vat_ppn = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    ppn_from_disbursement = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    loan_rate_lender = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    loan_rate_borrower = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    admin_fee = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    administration_cost = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    id_corporate = models.CharField(max_length=255, blank=True, null=True)
    status_corporate = models.CharField(max_length=50, blank=True, null=True)
    status_digisign = models.CharField(max_length=50, blank=True, null=True) # enum -> CharField
    id_marketing = models.CharField(max_length=255, blank=True, null=True)
    status_emergency = models.CharField(max_length=50, blank=True, null=True)
    topup = models.CharField(max_length=50, blank=True, null=True)
    unapproved_by = models.CharField(max_length=255, blank=True, null=True)
    channel = models.CharField(max_length=100, blank=True, null=True)
    pefindo_monthly_last_report_date = models.DateField(blank=True, null=True)
    is_ttd = models.IntegerField(blank=True, null=True) # int -> IntegerField, bisa juga BooleanField jika hanya 0/1
    recipient_account_name = models.CharField(max_length=255, blank=True, null=True)
    recipient_account_bank = models.CharField(max_length=100, blank=True, null=True)
    recipient_bank_id = models.CharField(max_length=100, blank=True, null=True)
    recipient_bank_branch = models.CharField(max_length=255, blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)
    recipient_status_rekening = models.CharField(max_length=50, blank=True, null=True) # enum -> CharField
    verification_at = models.DateTimeField(blank=True, null=True)
    verification_by = models.CharField(max_length=255, blank=True, null=True)
    status_verification = models.CharField(max_length=50, blank=True, null=True) # enum -> CharField
    canceled_by = models.CharField(max_length=255, blank=True, null=True)
    canceled_at = models.DateTimeField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'tb_fintech_borrower_loan'

    def __str__(self):
        return f"Loan {self.id_borrower_loan} by {self.register_code.register_code}"