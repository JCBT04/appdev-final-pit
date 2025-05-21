from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from readings.views import (
    BuildingViewSet,
    PowerReadingViewSet,
    RegisterUser,
    BuildingReadingsView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'buildings', BuildingViewSet)
router.register(r'readings', PowerReadingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', RegisterUser.as_view(), name='register_user'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/building-readings/', BuildingReadingsView.as_view(), name='building_readings'),
]