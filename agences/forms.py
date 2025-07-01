from django import forms
from .models import Agence

class AgenceForm(forms.ModelForm):
    class Meta:
        model = Agence
        exclude = ['id']
