from rest_framework import serializers
from .models import ConsumptionLog

class ConsumptionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumptionLog
        fields = '__all__'
