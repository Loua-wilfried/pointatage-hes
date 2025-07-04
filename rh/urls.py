from django.urls import path
from . import views

from .views import gestion_planning

from .views import gestion_absences, gestion_absences_crud, gestion_pointage, gestion_sanctions_crud, reporting_rh
from .views import export_reporting
from .views import formation
from .views import formation_crud

from .views.gestion_pointage import generate_qr_code

from .views.gestion_pointage import tableau_de_bord_pointage, ajouter_employe

urlpatterns = [
    path('planning/horaires/', gestion_planning.horaires_standard_list, name='horaires_standard_list'),
    path('planning/affectations/', gestion_planning.affectations_list, name='affectations_list'),
    path('planning/jours-feries/', gestion_planning.jours_feries_list, name='jours_feries_list'),
    path('planning/horaires-employes/', gestion_planning.horaires_employes_list, name='horaires_employes_list'),

    path('absences/', gestion_absences.absences_list, name='absences_list'),
    path('absences/types/', gestion_absences.types_absence_list, name='types_absence_list'),
    path('absences/demandes/', gestion_absences.demandes_conge_list, name='demandes_conge_list'),

    # CRUD AbsenceEmploye
    path('absences/nouvelle/', gestion_absences_crud.absence_create, name='absence_create'),
    path('absences/modifier/<int:pk>/', gestion_absences_crud.absence_update, name='absence_update'),
    path('absences/supprimer/<int:pk>/', gestion_absences_crud.absence_delete, name='absence_delete'),

    # CRUD TypeAbsence
    path('absences/types/nouveau/', gestion_absences_crud.typeabsence_create, name='typeabsence_create'),
    path('absences/types/modifier/<int:pk>/', gestion_absences_crud.typeabsence_update, name='typeabsence_update'),
    path('absences/types/supprimer/<int:pk>/', gestion_absences_crud.typeabsence_delete, name='typeabsence_delete'),

    # CRUD DemandeConge
    path('absences/demandes/nouvelle/', gestion_absences_crud.demandeconge_create, name='demandeconge_create'),
    path('absences/demandes/modifier/<int:pk>/', gestion_absences_crud.demandeconge_update, name='demandeconge_update'),
    path('absences/demandes/supprimer/<int:pk>/', gestion_absences_crud.demandeconge_delete, name='demandeconge_delete'),

    # CRUD Pointage
    path('pointages/', gestion_pointage.pointages_list, name='pointages_list'),
    path('pointage/add/', gestion_pointage.pointage_create, name='pointage_create'),
    path('pointage/<int:pk>/edit/', gestion_pointage.pointage_update, name='pointage_update'),
    path('pointage/<int:pk>/delete/', gestion_pointage.pointage_delete, name='pointage_delete'),
    path('tableau_de_bord_pointage/', tableau_de_bord_pointage, name='tableau_de_bord_pointage'),
    path('ajouter-employe/', ajouter_employe, name='ajouter_employe'),

    # Sanctions
    path('sanctions/', gestion_sanctions_crud.sanctions_list, name='sanctions_list'),
    path('sanction/add/', gestion_sanctions_crud.sanction_create, name='sanction_create'),
    path('sanction/<int:pk>/edit/', gestion_sanctions_crud.sanction_update, name='sanction_update'),
    path('sanction/<int:pk>/delete/', gestion_sanctions_crud.sanction_delete, name='sanction_delete'),

    # Génération QR Code pour Agent RH
    path('generer_qr/', generate_qr_code, name='generate_qr_code'),

    # Reporting RH
    path('reporting/', reporting_rh.reporting_rh, name='reporting_rh'),
    path('reporting/export/top-absents-excel/', export_reporting.export_top_absents_excel, name='export_top_absents_excel'),
    path('reporting/export/top-sanctionnes-excel/', export_reporting.export_top_sanctionnes_excel, name='export_top_sanctionnes_excel'),
    path('reporting/export/pdf/', export_reporting.export_reporting_pdf, name='export_reporting_pdf'),
    path('formations/', formation.formations_list, name='formations_list'),
    path('formations/add/', formation_crud.formation_create, name='formation_create'),
    path('formations/<int:pk>/edit/', formation_crud.formation_update, name='formation_update'),
    path('formations/<int:pk>/delete/', formation_crud.formation_delete, name='formation_delete'),
    path('formations/<int:formation_id>/sessions/', formation.sessions_list, name='sessions_list'),
    path('formations/<int:formation_id>/sessions/add/', formation_crud.session_create, name='session_create'),
    path('sessions/<int:pk>/edit/', formation_crud.session_update, name='session_update'),
    path('sessions/<int:pk>/delete/', formation_crud.session_delete, name='session_delete'),
    path('evaluations/', formation.evaluations_list, name='evaluations_list'),
    path('evaluations/add/', formation_crud.evaluation_create, name='evaluation_create'),
    path('evaluations/<int:pk>/edit/', formation_crud.evaluation_update, name='evaluation_update'),
    path('evaluations/<int:pk>/delete/', formation_crud.evaluation_delete, name='evaluation_delete'),
    path('evaluations/employe/<int:employe_id>/', formation.evaluations_list, name='evaluations_list_employe'),
    path('certifications/', formation.certifications_list, name='certifications_list'),
    path('certifications/add/', formation_crud.certification_create, name='certification_create'),
    path('certifications/<int:pk>/edit/', formation_crud.certification_update, name='certification_update'),
    path('certifications/<int:pk>/delete/', formation_crud.certification_delete, name='certification_delete'),
    path('certifications/employe/<int:employe_id>/', formation.certifications_list, name='certifications_list_employe'),
]
