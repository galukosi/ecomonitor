from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .models import Device, SensorReading, DeviceCommand
from .serializers import SensorReadingSerializer, DeviceSerializer
from django.shortcuts import get_object_or_404
import requests

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def sensor_reading(request):            
    """Receive data from ESP32 and check for commands"""
    try:
        data = request.data
        device_id = data.get('device_id')
        
        if not device_id:
            return Response({'error': 'device_id is required'}, status=400)
        
        try:
            device = Device.objects.get(device_id=device_id)
        except Device.DoesNotExist:
            return Response({
                'error': 'Device not registered', 
                'message': 'Please register this device on the website first'
            }, status=404)
        
        # Get or create device
        device, created = Device.objects.get_or_create(
            device_id=device_id,
            defaults={'name': f'Device {device_id}'}
        )
        
        # Update device status
        device.last_seen = timezone.now()
        device.save()
        
        # Check for pending commands
        pending_command = DeviceCommand.objects.filter(
            device=device, 
            executed=False
        ).order_by('created_at').first()
        

        if pending_command:
            response_data = {
                'command': pending_command.command_type,
                'payload': pending_command.payload
            }
            pending_command.executed = True
            pending_command.executed_at = timezone.now()
            pending_command.save()
            return Response(response_data)
        
        reading_data = {
            'final_value': data.get('final_value'),
            'raw_value': data.get('raw_value'),
            'voltage': data.get('voltage')
        }

        
        serializer = SensorReadingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            reading = serializer.save()
            check_for_alerts(device, reading)
            return Response({'status': 'success', 'reading_id': reading.id})
            return Response(serializer.errors, status=400)
    
        return Response({'status': 'success', 'message': 'No pending commands'})
    
    except Exception as e:
        return Response({'error': str(e)}, status=400)


def send_to_telegram(message, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

def check_for_alerts(device, reading):
    """Check if reading triggers any alerts"""
    if device.device_id.startswith('GG'):
        if reading.final_value > int(device.max_value_limit):
            send_to_telegram(f"""
⚠️ WARNING! ⚠️
⚠️ WARNING! ⚠️
⚠️ WARNING! ⚠️
                             
Device {device.name} detected excess CO!
CO level: {reading.final_value} ppm.
Evacuate everyone to fresh air and call emergency services from the outside!

Device ID: {device.device_id}.
""", device.telegram_bot_token, device.telegram_user_id),

    if device.device_id.startswith('TG'):
        if reading.final_value > device.max_value_limit:
            send_to_telegram(f"Warning! Too hot temperature: {reading.final_value} deegres", device.telegram_bot_token, device.telegram_user_id),
        elif reading.final_value < device.min_value_limit:
            send_to_telegram(f"Warning! Too cold temperature: {reading.final_value}", device.telegram_bot_token, device.telegram_user_id)

    if device.device_id.startswith('TG'):
            if reading.final_value > device.max_value_limit:
                send_to_telegram(f"Warning! Too hot temperature: {reading.final_value} deegres", device.telegram_bot_token, device.telegram_user_id),
            elif reading.final_value < device.min_value_limit:
                send_to_telegram(f"Warning! Too cold temperature: {reading.final_value}", device.telegram_bot_token, device.telegram_user_id)

class DeviceListAPIView(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceDetailAPIView(generics.RetrieveAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    lookup_field = 'device_id'

class SensorReadingListAPIView(generics.ListAPIView):
    serializer_class = SensorReadingSerializer
    
    def get_queryset(self):
        device_id = self.kwargs['device_id']
        return Reading.objects.filter(device__device_id=device_id).order_by('-created_at')[:100]
    
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def send_command_api(request):
    """API endpoint to send commands to devices"""
    device_id = request.data.get('device_id')
    command_type = request.data.get('command_type')
    payload = request.data.get('payload', '')
    
    if not device_id or not command_type:
        return Response({'error': 'device_id and command_type are required'}, status=400)
    
    device = get_object_or_404(Device, device_id=device_id, owner=request.user)
    
    command = DeviceCommand.objects.create(
        device=device,
        command_type=command_type,
        payload=payload
    )
    
    return Response({
        'status': 'command_queued', 
        'command_id': command.id,
        'device': device.device_id
    })
