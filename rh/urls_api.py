from django.urls import path
from rest_framework.routers import DefaultRouter
from rh.api import PointageViewSet

router = DefaultRouter()
router.register(r'pointages', PointageViewSet, basename='pointage')

from .views_api_auth import CustomTokenObtainPairView

urlpatterns = router.urls + [
    # Endpoint d'authentification JWT sécurisé
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
