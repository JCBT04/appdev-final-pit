from django.db import models

class ConsumptionLog(models.Model):
    building_name = models.CharField(max_length=100)
    appliance_name = models.CharField(max_length=100)
    consumption_kwh = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.building_name} - {self.appliance_name} at {self.timestamp}"