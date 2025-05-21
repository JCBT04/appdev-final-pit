from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ConsumptionLogViewSet,
    RegisterUserAPIView,
    CustomObtainAuthToken,
    PasswordResetAPIView,
    PasswordResetConfirmAPIView,
    BuildingViewSet,
    PowerReadingViewSet,
    BuildingReadingsView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'consumption-logs', ConsumptionLogViewSet, basename='consumptionlog')
router.register(r'buildings', BuildingViewSet)
router.register(r'readings', PowerReadingViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Auth and user registration
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('login/', CustomObtainAuthToken.as_view(), name='login'),
    path('forgot-password/', PasswordResetAPIView.as_view(), name='forgot-password'),
    path('reset-password-confirm/', PasswordResetConfirmAPIView.as_view(), name='reset-password-confirm'),

    # JWT Token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Custom API View for building readings
    path('building-readings/', BuildingReadingsView.as_view(), name='building_readings'),
]
