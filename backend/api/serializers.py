from rest_framework import serializers
from .models import Building, PowerReading

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'

class PowerReadingSerializer(serializers.ModelSerializer):
    building = BuildingSerializer(read_only=True)
    building_id = serializers.PrimaryKeyRelatedField(
        queryset=Building.objects.all(), source='building', write_only=True
    )

    class Meta:
        model = PowerReading
        fields = ['id', 'building', 'building_id', 'timestamp', 'voltage', 'current', 'power_kw']