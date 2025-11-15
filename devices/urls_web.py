from django.urls import path
from . import views_web

urlpatterns = [
    path('dashboard/', views_web.DashboardView.as_view(), name='dashboard'),
    path('<str:device_id>/', views_web.DeviceDetailView.as_view(), name='device-detail-web'),
    path('<str:device_id>/commands/', views_web.device_commands, name='device-commands'),
    path('<str:device_id>/commands/send/', views_web.send_command, name='send-command'),
    path('<str:device_id>/commands/history/', views_web.command_history, name='command-history'),
    path('<str:device_id>/readings/', views_web.readings_history, name='readings-history'),
    path("<str:device_id>/export-csv/", views_web.export_readings_csv, name="export-csv"),
    path("<str:device_id>/export-json/", views_web.export_readings_json, name="export-json"),
    path("<str:device_id>/clear-readings/", views_web.clear_readings, name="clear-readings"),
    path("<str:device_id>/settings/", views_web.device_settings, name="device-settings")
]