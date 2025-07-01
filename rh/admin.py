from django.contrib import admin
from .models import (
    DocumentRh, ContratTravail, HistoriquePoste, DonneeRhEmploye,
    HoraireStandard, HoraireEmploye, AffectationEmploye, JourFerie,
    TypeAbsence, AbsenceEmploye, DemandeConge, Pointage, Sanction,
    Formation, SessionFormation, Evaluation, CertificationEmploye
)

@admin.register(DocumentRh)
class DocumentRhAdmin(admin.ModelAdmin):
    list_display = ('employe', 'type_document', 'date_upload')
    search_fields = ('employe__nom', 'type_document')
    list_filter = ('type_document',)

@admin.register(ContratTravail)
class ContratTravailAdmin(admin.ModelAdmin):
    list_display = ('employe', 'type_contrat', 'date_debut', 'date_fin')
    search_fields = ('employe__nom', 'type_contrat')
    list_filter = ('type_contrat',)

@admin.register(HistoriquePoste)
class HistoriquePosteAdmin(admin.ModelAdmin):
    list_display = ('employe', 'poste', 'date_debut', 'date_fin', 'type_mouvement')
    search_fields = ('employe__nom', 'poste', 'type_mouvement')
    list_filter = ('type_mouvement',)

@admin.register(DonneeRhEmploye)
class DonneeRhEmployeAdmin(admin.ModelAdmin):
    list_display = ('employe', 'statut_rh', 'date_debut', 'date_fin')
    search_fields = ('employe__nom', 'statut_rh')
    list_filter = ('statut_rh',)

@admin.register(HoraireStandard)
class HoraireStandardAdmin(admin.ModelAdmin):
    list_display = ('nom', 'heure_debut', 'heure_fin', 'jours_semaine')
    search_fields = ('nom',)

@admin.register(HoraireEmploye)
class HoraireEmployeAdmin(admin.ModelAdmin):
    list_display = ('employe', 'horaire', 'date_debut', 'date_fin')
    search_fields = ('employe__nom', 'horaire__nom')

@admin.register(AffectationEmploye)
class AffectationEmployeAdmin(admin.ModelAdmin):
    list_display = ('employe', 'agence', 'date_debut', 'date_fin')
    search_fields = ('employe__nom', 'agence')

@admin.register(JourFerie)
class JourFerieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date', 'recurrence')
    search_fields = ('nom',)

@admin.register(TypeAbsence)
class TypeAbsenceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code')
    search_fields = ('nom', 'code')

@admin.register(AbsenceEmploye)
class AbsenceEmployeAdmin(admin.ModelAdmin):
    list_display = ('employe', 'type_absence', 'date_debut', 'date_fin', 'statut')
    search_fields = ('employe__nom', 'type_absence__nom', 'motif')
    list_filter = ('statut', 'type_absence')

@admin.register(DemandeConge)
class DemandeCongeAdmin(admin.ModelAdmin):
    list_display = ('employe', 'type_absence', 'date_debut', 'date_fin', 'statut', 'date_demande')
    search_fields = ('employe__nom', 'type_absence__nom')
    list_filter = ('statut', 'type_absence')

@admin.register(Pointage)
class PointageAdmin(admin.ModelAdmin):
    list_display = ('employe', 'date', 'heure', 'type', 'source', 'created_at')
    list_filter = ('type', 'source', 'date')
    search_fields = ('employe__nom', 'employe__prenom')

@admin.register(Sanction)
class SanctionAdmin(admin.ModelAdmin):
    list_display = ('employe', 'type', 'date', 'motif', 'duree', 'created_at')
    list_filter = ('type', 'date')
    search_fields = ('employe__nom', 'employe__prenom', 'motif')

@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'annee', 'description')
    search_fields = ('nom', 'annee')
    list_filter = ('annee',)

@admin.register(SessionFormation)
class SessionFormationAdmin(admin.ModelAdmin):
    list_display = ('formation', 'date_debut', 'date_fin', 'lieu', 'theme', 'intervenant')
    search_fields = ('formation__nom', 'lieu', 'theme', 'intervenant')
    list_filter = ('formation', 'date_debut', 'date_fin', 'lieu')

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('employe', 'session', 'note', 'date_evaluation')
    search_fields = ('employe__nom', 'session__formation__nom')
    list_filter = ('session', 'note')

@admin.register(CertificationEmploye)
class CertificationEmployeAdmin(admin.ModelAdmin):
    list_display = ('employe', 'session', 'certification', 'date_obtention', 'validee')
    search_fields = ('employe__nom', 'certification')
    list_filter = ('certification', 'validee', 'date_obtention')
