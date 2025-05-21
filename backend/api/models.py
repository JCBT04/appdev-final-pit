from django.db import models

class Building(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PowerReading(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    voltage = models.FloatField()
    current = models.FloatField()
    power_kw = models.FloatField()