from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('devices/', views.device_management, name='device-management'),
    path('devices/register/', views.register_device, name='register-device'),
    path('devices/<str:device_id>/unregister/', views.unregister_device, name='unregister-device'),
    path('devices/<str:device_id>/commands/', views.device_commands, name='device-commands'),
    path('devices/<str:device_id>/send-command/', views.send_device_command, name='send-command'),
]