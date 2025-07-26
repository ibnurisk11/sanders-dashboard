# core_dashboard/admin.py

from django.contrib import admin
from .models import TbFintechRegister, TbFintechBorrowerBio, TbFintechBorrowerLoan

# Daftarkan model Anda di sini
admin.site.register(TbFintechRegister)
admin.site.register(TbFintechBorrowerBio)
admin.site.register(TbFintechBorrowerLoan)