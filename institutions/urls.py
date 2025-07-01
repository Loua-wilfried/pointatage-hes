from django.urls import path
from .views import (
    InstitutionListView,
    InstitutionCreateView,
    InstitutionUpdateView,
    InstitutionDeleteView,
    PlanSaaSListView,
    PlanSaaSCreateView,
    PlanSaaSUpdateView,
    PlanSaaSDeleteView,
    AbonnementListView,
    AbonnementCreateView,
    AbonnementUpdateView,
    AbonnementDeleteView,
    AbonnementRenewView,
    AbonnementSuspendView,
    AbonnementResilierView,
    calculer_facture,
    EmployeListView
)

urlpatterns = [
    # Institutions
    path('', InstitutionListView.as_view(), name='institution_list'),

    # Employés (RH)
    path('ajouter/', InstitutionCreateView.as_view(), name='institution_create'),
    path('modifier/<int:pk>/', InstitutionUpdateView.as_view(), name='institution_update'),
    path('supprimer/<int:pk>/', InstitutionDeleteView.as_view(), name='institution_delete'),

    # Plans SaaS
    path('plans/', PlanSaaSListView.as_view(), name='plan_list'),
    path('plans/ajouter/', PlanSaaSCreateView.as_view(), name='plan_create'),
    path('plans/modifier/<int:pk>/', PlanSaaSUpdateView.as_view(), name='plan_update'),
    path('plans/supprimer/<int:pk>/', PlanSaaSDeleteView.as_view(), name='plan_delete'),

    # Abonnements
    path('abonnements/', AbonnementListView.as_view(), name='abonnement_list'),
    path('abonnements/ajouter/', AbonnementCreateView.as_view(), name='abonnement_create'),
    path('abonnements/modifier/<int:pk>/', AbonnementUpdateView.as_view(), name='abonnement_update'),
    path('abonnements/supprimer/<int:pk>/', AbonnementDeleteView.as_view(), name='abonnement_delete'),
    path('abonnements/renouveler/<int:pk>/', AbonnementRenewView.as_view(), name='abonnement_renew'),
    path('abonnements/suspendre/<int:pk>/', AbonnementSuspendView.as_view(), name='abonnement_suspend'),
    path('abonnements/resilier/<int:pk>/', AbonnementResilierView.as_view(), name='abonnement_resilier'),

    # Facturation
    path('calculer-facture/', calculer_facture, name='calculer_facture'),
]
