from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('institutions/', include('institutions.urls')),
    path('roles/', include('roles_permissions.urls')),
    path('agences/', include('agences.urls')),
    path('utilisateurs/', include('utilisateurs.urls')),
    path('rh/', include('rh.urls')),
    path('api/', include('rh.urls_api')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', include('utilisateurs.urls')),
    path('logout/', include('utilisateurs.urls')),
    path('', include('roles_permissions.urls_front')),
]

