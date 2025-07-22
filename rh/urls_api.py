from django.urls import path
from rest_framework.routers import DefaultRouter
from rh.api import PointageViewSet, AgenceViewSet, RoleViewSet

router = DefaultRouter()
router.register(r'pointages', PointageViewSet, basename='pointage')
router.register(r'agences', AgenceViewSet, basename='agence')
router.register(r'roles', RoleViewSet, basename='role')

from .views_api_auth import CustomTokenObtainPairView

urlpatterns = router.urls + [
    # Endpoint d'authentification JWT sécurisé
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
