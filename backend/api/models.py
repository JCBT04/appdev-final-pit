from django.db import models

class ConsumptionLog(models.Model):
    kwp = models.FloatField(default=0.0, help_text="Kilowatt peak")
    power = models.FloatField(default=0.0, help_text="Actual power consumption in watts")
    cost = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.kwp} kWp | {self.power} W | {self.consumption_kwh} kWh at {self.timestamp}"