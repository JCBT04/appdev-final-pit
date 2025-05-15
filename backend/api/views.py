from rest_framework import viewsets
from .models import ConsumptionLog
from .serializers import ConsumptionLogSerializer
from rest_framework.permissions import IsAuthenticated

class ConsumptionLogViewSet(viewsets.ModelViewSet):
    queryset = ConsumptionLog.objects.all().order_by('-timestamp')
    serializer_class = ConsumptionLogSerializer
    permission_classes = [IsAuthenticated]