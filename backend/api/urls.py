from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsumptionLogViewSet

router = DefaultRouter()
router.register(r'consumption', ConsumptionLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
