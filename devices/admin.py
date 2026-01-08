from django.contrib import admin
from django.utils import timezone
from .models import Device, SensorReading, DeviceCommand

@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ['device', 'final_value', 'created_at']
    list_filter = ['device', 'created_at']
    date_hierarchy = 'created_at'

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'device_model', 'name', 'last_seen']
    list_filter = ['created_at']
    search_fields = ['device_id', 'name']
    
@admin.action(description='Send command to selected devices')
def send_command(modeladmin, request, queryset):
    pass

class DeviceCommandInline(admin.TabularInline):
    model = DeviceCommand
    extra = 1
    readonly_fields = ('executed', 'executed_at')

class DeviceAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'name', 'owner', 'last_seen']
    list_filter = ['is_online', 'owner']
    actions = [send_command]
    inlines = [DeviceCommandInline]

class DeviceCommandAdmin(admin.ModelAdmin):
    list_display = ['device', 'command_type', 'executed', 'created_at']
    list_filter = ['command_type', 'executed', 'device']
    actions = ['mark_as_executed']

    def mark_as_executed(self, request, queryset):
        queryset.update(executed=True, executed_at=timezone.now())
        mark_as_executed.short_description = "Mark selected commands as executed"

admin.site.register(DeviceCommand, DeviceCommandAdmin)