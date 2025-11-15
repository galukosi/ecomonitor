from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views
from devices import views_web as devices_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('devices.urls')),
    path('dashboard/', devices_views.DashboardView.as_view(), name='dashboard'),
    path('devices/', include('devices.urls_web')),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('accounts/register/', accounts_views.register_view, name='register'),
    path('accounts/login/', accounts_views.login_view, name='login'),
    path('accounts/logout/', accounts_views.logout_view, name='logout'),
    path('accounts/profile/', accounts_views.profile_view, name='profile'),
    path('accounts/change-password/', accounts_views.change_password_view, name='change_password'),
    path('accounts/devices/', accounts_views.device_management, name='device-management'),
    path('accounts/devices/register/', accounts_views.register_device, name='register-device'),
    path('accounts/devices/<str:device_id>/unregister/', accounts_views.unregister_device, name='unregister-device') 
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)