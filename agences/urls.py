from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_agences, name='liste_agences'),
    path('nouveau/', views.creer_agence, name='creer_agence'),
    path('modifier/<str:id>/', views.modifier_agence, name='modifier_agence'),
    path('supprimer/<str:id>/', views.supprimer_agence, name='supprimer_agence'),
]
