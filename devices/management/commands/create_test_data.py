from django.core.management.base import BaseCommand
from django.utils import timezone
from devices.models import Device, GasReading
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Create test data for development'

    def handle(self, *args, **options):
        # Create test devices
        devices = []
        for i in range(3):
            device, created = Device.objects.get_or_create(
                device_id=f'GG-TEST-{i+1:03d}',
                defaults={
                    'name': f'Test Device {i+1}',
                    'location': f'Location {i+1}',
                    'is_online': True,
                    'last_seen': timezone.now()
                }
            )
            devices.append(device)
        
        # Create test readings
        for device in devices:
            for hours_ago in range(24 * 7):  # 7 days of data
                timestamp = timezone.now() - timedelta(hours=hours_ago)
                ppm = random.uniform(5, 150)
                
                GasReading.objects.create(
                    device=device,
                    ppm=ppm,
                    raw_value=int(random.uniform(100, 1000)),
                    voltage=random.uniform(2.5, 3.3),
                    timestamp=int(timestamp.timestamp() * 1000),
                    created_at=timestamp
                )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created test data')
        )