from django import forms
from .models import Institution, PlanSaaS, Abonnement, Employe
from django import forms
from django.utils import timezone
from datetime import timedelta, date

class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        exclude = ['code_institution', 'date_creation']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'pays': forms.TextInput(attrs={'class': 'form-control'}),
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'indicatif_pays': forms.TextInput(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
        }

class PlanSaaSForm(forms.ModelForm):
    class Meta:
        model = PlanSaaS
        fields = ['nom_plan', 'description', 'prix_mensuel', 'limite_utilisateurs', 'fonctionnalites_incluses']
        widgets = {
            'nom_plan': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'prix_mensuel': forms.NumberInput(attrs={'class': 'form-control'}),
            'limite_utilisateurs': forms.NumberInput(attrs={'class': 'form-control'}),
            'fonctionnalites_incluses': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ex: ["Export PDF", "Support prioritaire", ...]'}),
        }

    def clean_fonctionnalites_incluses(self):
        import json
        data = self.cleaned_data['fonctionnalites_incluses']
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception:
                raise forms.ValidationError("Veuillez entrer une liste JSON valide (ex: ['Export PDF', 'Support prioritaire'])")
        return data

class AbonnementForm(forms.ModelForm):
    duree_mois = forms.IntegerField(min_value=1, initial=1, label="Durée (mois)", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Abonnement
        fields = ['institution', 'plan', 'date_debut', 'mode_paiement', 'duree_mois']
        widgets = {
            'institution': forms.Select(attrs={'class': 'form-select'}),
            'plan': forms.Select(attrs={'class': 'form-select'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'mode_paiement': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        duree_mois = cleaned_data.get('duree_mois')
        if date_debut and duree_mois:
            # Logique de validation personnalisée ici
            pass
        return cleaned_data

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = [
            'prenom', 'nom', 'sexe', 'date_naissance', 'lieu_naissance', 'nationalite',
            'situation_familiale', 'adresse', 'email', 'telephone', 'numero_cni', 'photo',
            'date_embauche', 'date_fin_contrat', 'type_contrat', 'periode_essai',
            'agence', 'role', 'statut', 'horaire_travail', 'salaire_base', 'rib_banque'
        ]
        widgets = {
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'sexe': forms.Select(attrs={'class': 'form-select'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lieu_naissance': forms.TextInput(attrs={'class': 'form-control'}),
            'nationalite': forms.TextInput(attrs={'class': 'form-control'}),
            'situation_familiale': forms.Select(attrs={'class': 'form-select'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_cni': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date_embauche': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_contrat': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'type_contrat': forms.Select(attrs={'class': 'form-select'}),
            'periode_essai': forms.TextInput(attrs={'class': 'form-control'}),
            'agence': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'horaire_travail': forms.TextInput(attrs={'class': 'form-control'}),
            'salaire_base': forms.NumberInput(attrs={'class': 'form-control'}),
            'rib_banque': forms.TextInput(attrs={'class': 'form-control'}),
        }

    class Meta:
        model = Employe
        fields = [
            'prenom', 'nom', 'sexe', 'date_naissance', 'lieu_naissance', 'nationalite',
            'situation_familiale', 'adresse', 'email', 'telephone', 'numero_cni', 'photo',
            'date_embauche', 'date_fin_contrat', 'type_contrat', 'periode_essai',
            'agence', 'role', 'statut', 'horaire_travail', 'salaire_base', 'rib_banque'
        ]
        widgets = {
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'sexe': forms.Select(attrs={'class': 'form-select'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lieu_naissance': forms.TextInput(attrs={'class': 'form-control'}),
            'nationalite': forms.TextInput(attrs={'class': 'form-control'}),
            'situation_familiale': forms.Select(attrs={'class': 'form-select'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_cni': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date_embauche': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_contrat': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'type_contrat': forms.Select(attrs={'class': 'form-select'}),
            'periode_essai': forms.TextInput(attrs={'class': 'form-control'}),
            'agence': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'horaire_travail': forms.TextInput(attrs={'class': 'form-control'}),
            'salaire_base': forms.NumberInput(attrs={'class': 'form-control'}),
            'rib_banque': forms.TextInput(attrs={'class': 'form-control'}),
        }

    class Meta:
        model = Employe
        fields = ['prenom', 'nom', 'email', 'telephone', 'agence', 'role', 'date_embauche', 'statut']
        widgets = {
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'agence': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'date_embauche': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
        }

    duree_mois = forms.IntegerField(min_value=1, initial=1, label="Durée (mois)", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Abonnement
        fields = ['institution', 'plan', 'date_debut', 'mode_paiement', 'duree_mois']
        widgets = {
            'institution': forms.Select(attrs={'class': 'form-select'}),
            'plan': forms.Select(attrs={'class': 'form-select'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'mode_paiement': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        duree_mois = cleaned_data.get('duree_mois')
        if date_debut and duree_mois:
            # Calcule la date de fin automatiquement
            mois = int(duree_mois)
            # Gestion du passage d'année/mois
            annee = date_debut.year + ((date_debut.month - 1 + mois) // 12)
            mois_final = ((date_debut.month - 1 + mois) % 12) + 1
            jour = min(date_debut.day, [31,29 if annee%4==0 and (annee%100!=0 or annee%400==0) else 28,31,30,31,30,31,31,30,31,30,31][mois_final-1])
            date_fin = date(annee, mois_final, jour)
            cleaned_data['date_fin'] = date_fin
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.date_fin = self.cleaned_data['date_fin']
        # Statut initial
        if instance.date_debut <= timezone.now().date():
            instance.statut = 'actif'
        else:
            instance.statut = 'en_attente'
        if commit:
            instance.save()
        return instance
