from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from rh.models import HoraireStandard, AffectationEmploye, JourFerie, HoraireEmploye

@login_required
@permission_required('rh.view_horairestandard', raise_exception=True)
def horaires_standard_list(request):
    horaires = HoraireStandard.objects.all()
    return render(request, 'rh/planning/horaires_standard_list.html', {'horaires': horaires})

@login_required
@permission_required('rh.view_affectationemploye', raise_exception=True)
def affectations_list(request):
    affectations = AffectationEmploye.objects.select_related('employe').all()
    return render(request, 'rh/planning/affectations_list.html', {'affectations': affectations})

@login_required
@permission_required('rh.view_jourferie', raise_exception=True)
def jours_feries_list(request):
    jours = JourFerie.objects.all()
    return render(request, 'rh/planning/jours_feries_list.html', {'jours': jours})

@login_required
@permission_required('rh.view_horaireemploye', raise_exception=True)
def horaires_employes_list(request):
    horaires = HoraireEmploye.objects.select_related('employe', 'horaire').all()
    return render(request, 'rh/planning/horaires_employes_list.html', {'horaires_employes': horaires})
