from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from rh.models import Formation, SessionFormation, Evaluation, CertificationEmploye
from rh.forms import FormationForm, SessionFormationForm, EvaluationForm, CertificationEmployeForm

# FORMATION CRUD
@login_required
@permission_required('rh.add_formation', raise_exception=True)
def formation_create(request):
    if request.method == 'POST':
        form = FormationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Formation ajoutée avec succès.")
            return redirect('formations_list')
    else:
        form = FormationForm()
    return render(request, 'rh/formation/formation_form.html', {'form': form, 'action': 'Ajouter'})

@login_required
@permission_required('rh.change_formation', raise_exception=True)
def formation_update(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    if request.method == 'POST':
        form = FormationForm(request.POST, instance=formation)
        if form.is_valid():
            form.save()
            messages.success(request, "Formation modifiée avec succès.")
            return redirect('formations_list')
    else:
        form = FormationForm(instance=formation)
    return render(request, 'rh/formation/formation_form.html', {'form': form, 'action': 'Modifier'})

@login_required
@permission_required('rh.delete_formation', raise_exception=True)
def formation_delete(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    if request.method == 'POST':
        formation.delete()
        messages.success(request, "Formation supprimée.")
        return redirect('formations_list')
    return render(request, 'rh/formation/formation_confirm_delete.html', {'formation': formation})

# SESSION CRUD
@login_required
@permission_required('rh.add_sessionformation', raise_exception=True)
def session_create(request, formation_id):
    if request.method == 'POST':
        form = SessionFormationForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.formation_id = formation_id
            session.save()
            messages.success(request, "Session ajoutée.")
            return redirect('sessions_list', formation_id=formation_id)
    else:
        form = SessionFormationForm(initial={'formation': formation_id})
    return render(request, 'rh/formation/session_form.html', {'form': form, 'action': 'Ajouter', 'formation_id': formation_id})

@login_required
@permission_required('rh.change_sessionformation', raise_exception=True)
def session_update(request, pk):
    session = get_object_or_404(SessionFormation, pk=pk)
    if request.method == 'POST':
        form = SessionFormationForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, "Session modifiée.")
            return redirect('sessions_list', formation_id=session.formation_id)
    else:
        form = SessionFormationForm(instance=session)
    return render(request, 'rh/formation/session_form.html', {'form': form, 'action': 'Modifier', 'formation_id': session.formation_id})

@login_required
@permission_required('rh.delete_sessionformation', raise_exception=True)
def session_delete(request, pk):
    session = get_object_or_404(SessionFormation, pk=pk)
    formation_id = session.formation_id
    if request.method == 'POST':
        session.delete()
        messages.success(request, "Session supprimée.")
        return redirect('sessions_list', formation_id=formation_id)
    return render(request, 'rh/formation/session_confirm_delete.html', {'session': session, 'formation_id': formation_id})

# EVALUATION CRUD
@login_required
@permission_required('rh.add_evaluation', raise_exception=True)
def evaluation_create(request):
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Évaluation ajoutée.")
            return redirect('evaluations_list')
    else:
        form = EvaluationForm()
    return render(request, 'rh/formation/evaluation_form.html', {'form': form, 'action': 'Ajouter'})

@login_required
@permission_required('rh.change_evaluation', raise_exception=True)
def evaluation_update(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk)
    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            messages.success(request, "Évaluation modifiée.")
            return redirect('evaluations_list')
    else:
        form = EvaluationForm(instance=evaluation)
    return render(request, 'rh/formation/evaluation_form.html', {'form': form, 'action': 'Modifier'})

@login_required
@permission_required('rh.delete_evaluation', raise_exception=True)
def evaluation_delete(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk)
    if request.method == 'POST':
        evaluation.delete()
        messages.success(request, "Évaluation supprimée.")
        return redirect('evaluations_list')
    return render(request, 'rh/formation/evaluation_confirm_delete.html', {'evaluation': evaluation})

# CERTIFICATION CRUD
@login_required
@permission_required('rh.add_certificationemploye', raise_exception=True)
def certification_create(request):
    if request.method == 'POST':
        form = CertificationEmployeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Certification ajoutée.")
            return redirect('certifications_list')
    else:
        form = CertificationEmployeForm()
    return render(request, 'rh/formation/certification_form.html', {'form': form, 'action': 'Ajouter'})

@login_required
@permission_required('rh.change_certificationemploye', raise_exception=True)
def certification_update(request, pk):
    certification = get_object_or_404(CertificationEmploye, pk=pk)
    if request.method == 'POST':
        form = CertificationEmployeForm(request.POST, instance=certification)
        if form.is_valid():
            form.save()
            messages.success(request, "Certification modifiée.")
            return redirect('certifications_list')
    else:
        form = CertificationEmployeForm(instance=certification)
    return render(request, 'rh/formation/certification_form.html', {'form': form, 'action': 'Modifier'})

@login_required
@permission_required('rh.delete_certificationemploye', raise_exception=True)
def certification_delete(request, pk):
    certification = get_object_or_404(CertificationEmploye, pk=pk)
    if request.method == 'POST':
        certification.delete()
        messages.success(request, "Certification supprimée.")
        return redirect('certifications_list')
    return render(request, 'rh/formation/certification_confirm_delete.html', {'certification': certification})
