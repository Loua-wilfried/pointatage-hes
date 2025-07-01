from django.urls import path
from . import views_front

urlpatterns = [
    path('', views_front.home, name='home'),
    # Rôles
    path('roles/', views_front.roles_list, name='roles_list'),
    path('roles/ajouter/', views_front.role_create, name='role_create'),
    path('roles/<int:pk>/modifier/', views_front.role_edit, name='role_edit'),
    path('roles/<int:pk>/supprimer/', views_front.role_delete, name='role_delete'),
    # Permissions
    path('permissions/', views_front.permissions_list, name='permissions_list'),
    path('permissions/ajouter/', views_front.permission_create, name='permission_create'),
    path('permissions/<int:pk>/modifier/', views_front.permission_edit, name='permission_edit'),
    path('permissions/<int:pk>/supprimer/', views_front.permission_delete, name='permission_delete'),
    # Affectations
    path('affectations/', views_front.affectations_list, name='affectations_list'),
    path('affectations/ajouter/', views_front.affectation_create, name='affectation_create'),
    path('affectations/<int:pk>/supprimer/', views_front.affectation_delete, name='affectation_delete'),
    path('affectations/visuelle/', views_front.affectation_visuelle, name='affectation_visuelle'),
    # UserRoles
    path('userroles/', views_front.userroles_list, name='userroles_list'),
]
