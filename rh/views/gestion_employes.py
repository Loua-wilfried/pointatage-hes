from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from rh.models import DocumentRh, ContratTravail, HistoriquePoste, DonneeRhEmploye
from rh.forms import DocumentRhForm, ContratTravailForm, HistoriquePosteForm, DonneeRhEmployeForm
from institutions.models import Employe

# Exemple : Liste des documents RH pour un employé
@login_required
@permission_required('rh.view_documentrh', raise_exception=True)
def documents_employe(request, employe_id):
    employe = get_object_or_404(Employe, pk=employe_id)
    documents = DocumentRh.objects.filter(employe=employe)
    return render(request, 'rh/gestion_employes/documents_list.html', {'employe': employe, 'documents': documents})

# Ajout, édition, suppression, etc. à compléter selon les besoins
