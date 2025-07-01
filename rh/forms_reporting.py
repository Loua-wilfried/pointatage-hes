from django import forms
from institutions.models import Employe

class ReportingRHFilterForm(forms.Form):
    employe = forms.ModelChoiceField(queryset=Employe.objects.all(), required=False, label="Employé")
    date_debut = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date début")
    date_fin = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date fin")
    type_evenement = forms.ChoiceField(
        choices=[('', 'Tous'), ('absence', 'Absence'), ('sanction', 'Sanction'), ('pointage', 'Pointage')],
        required=False,
        label="Type d'événement"
    )
