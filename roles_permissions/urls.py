from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, PermissionViewSet, RolePermissionViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'role-permissions', RolePermissionViewSet)

from . import views

urlpatterns = [
    # API endpoints (DRF)
    path('api/', include(router.urls)),

    # HTML endpoints (pour navigation humaine)
    path('roles/', views.role_list, name='role_list'),
    path('roles/nouveau/', views.role_create, name='role_create'),
    path('roles/modifier/<int:pk>/', views.role_update, name='role_update'),
    path('roles/supprimer/<int:pk>/', views.role_delete, name='role_delete'),
]

