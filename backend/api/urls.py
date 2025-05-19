from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsumptionLogViewSet, RegisterUserAPIView, CustomObtainAuthToken, PasswordResetAPIView, PasswordResetConfirmAPIView

router = DefaultRouter()
router.register('consumption-logs', ConsumptionLogViewSet, basename='consumptionlog')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('login/', CustomObtainAuthToken.as_view(), name='login'),
    path('forgot-password/', PasswordResetAPIView.as_view(), name='forgot-password'),
    path('reset-password-confirm/', PasswordResetConfirmAPIView.as_view(), name='reset-password-confirm'),
]

