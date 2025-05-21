from rest_framework import viewsets
from .models import Building, PowerReading
from .serializers import BuildingSerializer, PowerReadingSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

class PowerReadingViewSet(viewsets.ModelViewSet):
    queryset = PowerReading.objects.all().order_by('-timestamp')
    serializer_class = PowerReadingSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    @action(detail=False, methods=['get'])
    def average_power(self, request):
        data = PowerReading.objects.values('building__name').annotate(avg_power=Avg('power_kw'))
        return Response(data)

    def create(self, request, *args, **kwargs):
        building_id = request.data.get("building_id")
        if building_id is not None:
            Building.objects.get_or_create(id=building_id, defaults={"name": f"AutoCreated Building {building_id}"})
        return super().create(request, *args, **kwargs)

class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class RegisterUser(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]



from rest_framework.generics import ListAPIView

class BuildingReadingsView(ListAPIView):
    serializer_class = PowerReadingSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        building_id = self.request.query_params.get('building_id')
        return PowerReading.objects.filter(building_id=building_id).order_by('-timestamp')[:10]