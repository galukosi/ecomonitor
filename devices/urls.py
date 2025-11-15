from django.urls import path
from . import views

urlpatterns = [
    path('sensor-readings/', views.sensor_reading, name='sensor-reading'),
    path('send-command/', views.send_command_api, name='send-command-api'),
    path('devices/', views.DeviceListAPIView.as_view(), name='device-list'),
    path('devices/<str:device_id>/', views.DeviceDetailAPIView.as_view(), name='device-detail'),
    path('devices/<str:device_id>/commands/', views.send_command_api, name='send-command-api'),
    path('devices/<str:device_id>/readings/', views.SensorReadingListAPIView.as_view(), name='device-readings'),
]