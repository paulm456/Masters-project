from django.contrib import admin
from .models import SensorReading

# Register your models here.
@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ('pm1', 'pm25', 'pm10', 'timestamp')
    ordering = ('-timestamp',)