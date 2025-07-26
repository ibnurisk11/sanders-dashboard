# core_dashboard/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Halaman utama (HTML)
    path('users/', views.user_list_api, name='user_list_api'),
    path('users/<str:register_code_param>/', views.user_detail_api, name='user_detail_api'),
    path('loans/', views.loan_list_api, name='loan_list_api'), # Endpoint untuk daftar pinjaman
]