from django import forms
from django.contrib.auth.models import User
# Forms : Utilisez uniquement les formulaires liés à User natif de Django.
from roles_permissions.models import Role
from agences.models import Agence

class UtilisateurCreationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'telephone', 'agence', 'role', 'statut_utilisateur', 'photo']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Cet email est déjà utilisé.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Les mots de passe ne correspondent pas.')
        return cleaned_data

class UtilisateurChangeForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'telephone', 'agence', 'role', 'statut_utilisateur', 'photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if self.instance and self.instance.user:
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise forms.ValidationError('Cet email est déjà utilisé.')
        return email

class ConnexionForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ChangerMotDePasseForm(forms.Form):
    password1 = forms.CharField(label='Nouveau mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmer le nouveau mot de passe', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Les mots de passe ne correspondent pas.')
        return cleaned_data
