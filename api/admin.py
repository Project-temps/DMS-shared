from django.contrib import admin

from .models import Farm, SensorReading

admin.site.register(Farm)
admin.site.register(SensorReading)
