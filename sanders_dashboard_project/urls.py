# sanders_dashboard_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # Import Django's auth views

urlpatterns = [
    path('admin/', admin.site.urls),
    # URL untuk login dan logout
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', include('core_dashboard.urls')), # Pastikan ini di akhir
]