from django.contrib import admin
from .models import Institution, PlanSaaS, Abonnement, Employe

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('code_institution', 'nom', 'pays', 'ville', 'statut', 'date_creation')
    search_fields = ('code_institution', 'nom', 'pays', 'ville')
    list_filter = ('pays', 'ville', 'statut')
    readonly_fields = ('code_institution', 'date_creation')

@admin.register(PlanSaaS)
class PlanSaaSAdmin(admin.ModelAdmin):
    list_display = ('nom_plan', 'prix_mensuel', 'limite_utilisateurs')
    search_fields = ('nom_plan',)

@admin.register(Abonnement)
class AbonnementAdmin(admin.ModelAdmin):
    list_display = ('institution', 'plan', 'date_debut', 'date_fin', 'statut', 'mode_paiement')
    list_filter = ('statut', 'plan')
    search_fields = ('institution__nom', 'plan__nom_plan')

@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'matricule_interne', 'agence', 'role', 'statut', 'date_embauche')
    list_filter = ('agence', 'role', 'statut')
    search_fields = ('nom', 'prenom', 'matricule_interne', 'email')
    readonly_fields = ('matricule_interne', 'date_creation')

    def get_readonly_fields(self, request, obj=None):
        # Champs sensibles visibles uniquement en édition par superuser
        base = list(super().get_readonly_fields(request, obj))
        sensibles = ['salaire_base', 'sanctions', 'solde_tout_compte']
        if not request.user.is_superuser:
            base += sensibles
        return base
