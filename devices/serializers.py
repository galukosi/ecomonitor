from django.utils import timezone
from rest_framework import serializers
from .models import Device, SensorReading, DeviceCommand
from django.contrib.auth.models import User

class SensorReadingSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(write_only=True)

    class Meta:
        model = SensorReading
        fields = ['id', 'device', 'device_id', 'final_value', 'created_at']
        read_only_fields = ('device', 'created_at')

    def create(self, validated_data):
        # Taking device_id from JSON
        device_id = validated_data.pop('device_id')

        # Taking user if exists (e.g. web login)
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None

        # Create/find device
        device, _ = Device.objects.get_or_create(
            device_id=device_id,
            defaults={
                'name': f'My device {device_id[-6:]}',
                'owner': user
            }
        )
        
        # Update last_seen
        device.last_seen = timezone.now()
        device.save()

        # Save the readings
        validated_data['device'] = device
        return SensorReading.objects.create(**validated_data)


class DeviceSerializer(serializers.ModelSerializer):
    latest_reading = serializers.SerializerMethodField()
    reading_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Device
        fields = '__all__'
        read_only_fields = ('owner', 'created_at', 'updated_at')
    
    def get_latest_reading(self, obj):
        latest = obj.readings.order_by('-created_at').first()
        if latest:
            return {
                'final_value': latest.final_value,
                'created_at': latest.created_at
            }
        return None
    
    def get_reading_count(self, obj):
        return obj.readings.count()
class DeviceCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceCommand
        fields = '__all__'