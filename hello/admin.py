import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import SensorReading

def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=sensor_readings.csv'

    writer = csv.writer(response)
    writer.writerow([
        'Timestamp',
        'PM1',
        'PM2.5',
        'PM10',
    ])

    for reading in queryset:
        writer.writerow([
            reading.timestamp,
            reading.pm1,
            reading.pm25,
            reading.pm10
        ])


    return response

# Register your models here.
@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'pm1', 'pm25', 'pm10')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)
    actions = [export_as_csv]



export_as_csv.short_description = "Export selected rows as CSV"