from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Device(models.Model):
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='devices',
        null=True, blank=True
    )

    device_id = models.CharField(max_length=50, unique=True)
    device_model = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=100, default='My Device')
    last_seen = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reading_time = models.IntegerField(validators=[MinValueValidator(1)], default=15)
    min_value_limit = models.IntegerField(blank=True)
    max_value_limit = models.IntegerField()
    telegram_user_id = models.CharField(max_length=100, blank=True)
    telegram_bot_token = models.CharField(max_length=100, blank=True)

    @property
    def is_online(self):
        return (
            self.last_seen is not None
            and (timezone.now() - self.last_seen).total_seconds() < 300
        )
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.device_id}) - {self.owner.email}"
    
    def save(self, *args, **kwargs):
        if self.pk is None and self.device_id:
            if self.device_id.startswith("GG"):
                self.device_model = "GasGuard"
                self.min_value_limit = 0
                self.max_value_limit = 100
            elif self.device_id.startswith("TG"):
                self.device_model = "TempGuard"
                self.min_value_limit = 18
                self.max_value_limit = 26
            elif self.device_id.startswith("HG"):
                self.device_model = "HumidGuard"
                self.min_value_limit = 30
                self.max_value_limit = 60
            else:
                self.device_model = "Unknown"
                self.min_value_limit = 0
                self.max_value_limit = 0

        super().save(*args, **kwargs)

    

class SensorReading(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='readings')
    final_value = models.FloatField()
    raw_value = models.IntegerField(null=True, blank=True)
    voltage = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.device.device_id} - {self.final_value} ppm"

class DeviceCommand(models.Model):
    COMMAND_TYPES = [
        ('clear_eeprom', 'Clear EEPROM'),
        ('restart', 'Restart Device'),
        ('enable_screen', 'Enable Screen'),
        ('disable_screen', 'Disable Screen'),
        ('update_api_url', 'Update API URL'),
        ('change_reading_time', 'Change Reading Time'),
        ('display_message', 'Display Message'),
        ('calibrate_sensor', 'Calibrate Sensor'),
        ('reboot', 'Reboot Device'),
        ('factory_reset', 'Factory Reset'),
    ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='commands')
    command_type = models.CharField(max_length=50, choices=COMMAND_TYPES)
    payload = models.TextField(blank=True)
    executed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    executed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.device.device_id} - {self.command_type}"