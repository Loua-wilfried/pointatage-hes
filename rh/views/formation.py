from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from rh.models import Formation, SessionFormation, Evaluation, CertificationEmploye
from institutions.models import Employe
from rh.forms import FormationForm, SessionFormationForm, EvaluationForm, CertificationEmployeForm

@login_required
@permission_required('rh.view_formation', raise_exception=True)
def formations_list(request):
    formations = Formation.objects.all().order_by('-annee', 'nom')
    return render(request, 'rh/formation/formations_list.html', {'formations': formations})

@login_required
@permission_required('rh.view_sessionformation', raise_exception=True)
def sessions_list(request, formation_id):
    formation = get_object_or_404(Formation, pk=formation_id)
    sessions = SessionFormation.objects.filter(formation=formation)
    return render(request, 'rh/formation/sessions_list.html', {'sessions': sessions, 'formation': formation})

@login_required
@permission_required('rh.view_evaluation', raise_exception=True)
def evaluations_list(request, employe_id=None):
    if employe_id:
        employe = get_object_or_404(Employe, pk=employe_id)
        evaluations = Evaluation.objects.filter(employe=employe)
    else:
        employe = None
        evaluations = Evaluation.objects.all()
    return render(request, 'rh/formation/evaluations_list.html', {'evaluations': evaluations, 'employe': employe})

@login_required
@permission_required('rh.view_certificationemploye', raise_exception=True)
def certifications_list(request, employe_id=None):
    if employe_id:
        employe = get_object_or_404(Employe, pk=employe_id)
        certifications = CertificationEmploye.objects.filter(employe=employe)
    else:
        employe = None
        certifications = CertificationEmploye.objects.all()
    return render(request, 'rh/formation/certifications_list.html', {'certifications': certifications, 'employe': employe})
