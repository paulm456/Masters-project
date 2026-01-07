from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class LogMessage(models.Model):
    message = models.CharField(max_length=300)
    log_date = models.DateTimeField("date logged")

    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"
    

class SensorReading(models.Model):
    pm1 = models.FloatField()
    pm25 = models.FloatField()
    pm10 = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"PM1: {self.pm1}, PM2.5: {self.pm25}, PM10: {self.pm10} @ {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
