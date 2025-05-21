from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API app routes (includes viewsets + auth + password management)
    path('api/', include('api.urls')),

    # Optionally: DRF's built-in token auth if still needed
    # This is separate from JWT and CustomObtainAuthToken
    # You may remove this if you're fully using JWT/custom login
    path('api-token-auth/', include('rest_framework.urls')),
]
