from django.contrib import admin
from .models import Building, PowerReading

admin.site.register(Building)
admin.site.register(PowerReading)