from django import forms
from .models import (
    DocumentRh, ContratTravail, HistoriquePoste, DonneeRhEmploye,
    HoraireStandard, HoraireEmploye, AffectationEmploye, JourFerie,
    TypeAbsence, AbsenceEmploye, DemandeConge, Pointage, Sanction,
    Formation, SessionFormation, Evaluation, CertificationEmploye
)

class DocumentRhForm(forms.ModelForm):
    class Meta:
        model = DocumentRh
        fields = ['employe', 'type_document', 'fichier', 'commentaire']

class ContratTravailForm(forms.ModelForm):
    class Meta:
        model = ContratTravail
        fields = ['employe', 'type_contrat', 'date_debut', 'date_fin', 'fichier_contrat', 'statut']

class HistoriquePosteForm(forms.ModelForm):
    class Meta:
        model = HistoriquePoste
        fields = ['employe', 'poste', 'agence', 'date_debut', 'date_fin', 'type_mouvement', 'commentaire']

class DonneeRhEmployeForm(forms.ModelForm):
    class Meta:
        model = DonneeRhEmploye
        fields = ['employe', 'statut_rh', 'date_debut', 'date_fin', 'commentaire']

class HoraireStandardForm(forms.ModelForm):
    class Meta:
        model = HoraireStandard
        fields = ['nom', 'description', 'heure_debut', 'heure_fin', 'jours_semaine']

class HoraireEmployeForm(forms.ModelForm):
    class Meta:
        model = HoraireEmploye
        fields = ['employe', 'horaire', 'date_debut', 'date_fin', 'commentaire']

class AffectationEmployeForm(forms.ModelForm):
    class Meta:
        model = AffectationEmploye
        fields = ['employe', 'agence', 'date_debut', 'date_fin', 'commentaire']

class JourFerieForm(forms.ModelForm):
    class Meta:
        model = JourFerie
        fields = ['nom', 'date', 'recurrence', 'commentaire']

class TypeAbsenceForm(forms.ModelForm):
    class Meta:
        model = TypeAbsence
        fields = ['nom', 'code', 'description']

class AbsenceEmployeForm(forms.ModelForm):
    class Meta:
        model = AbsenceEmploye
        fields = ['employe', 'type_absence', 'date_debut', 'date_fin', 'motif', 'statut', 'justificatif', 'commentaire']

class DemandeCongeForm(forms.ModelForm):
    class Meta:
        model = DemandeConge
        fields = ['employe', 'date_debut', 'date_fin', 'type_absence', 'statut', 'commentaire']

class PointageForm(forms.ModelForm):
    class Meta:
        model = Pointage
        fields = ['employe', 'date', 'heure', 'type', 'source', 'commentaire']

class SanctionForm(forms.ModelForm):
    class Meta:
        model = Sanction
        fields = ['employe', 'type', 'date', 'motif', 'duree', 'commentaire', 'justificatif']

class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['nom', 'description', 'annee']

class SessionFormationForm(forms.ModelForm):
    class Meta:
        model = SessionFormation
        fields = ['formation', 'date_debut', 'date_fin', 'lieu', 'theme', 'intervenant']

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['employe', 'session', 'note', 'commentaire']

class CertificationEmployeForm(forms.ModelForm):
    class Meta:
        model = CertificationEmploye
        fields = ['employe', 'session', 'certification', 'date_obtention', 'validee']
