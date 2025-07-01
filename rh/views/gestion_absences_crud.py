from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from rh.models import AbsenceEmploye, TypeAbsence, DemandeConge
from rh.forms import AbsenceEmployeForm, TypeAbsenceForm, DemandeCongeForm

# --- AbsenceEmploye CRUD ---
@login_required
@permission_required('rh.add_absenceemploye', raise_exception=True)
def absence_create(request):
    if request.method == 'POST':
        form = AbsenceEmployeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('absences_list')
    else:
        form = AbsenceEmployeForm()
    return render(request, 'rh/absences/absence_form.html', {'form': form, 'action': 'Créer'})

@login_required
@permission_required('rh.change_absenceemploye', raise_exception=True)
def absence_update(request, pk):
    absence = get_object_or_404(AbsenceEmploye, pk=pk)
    if request.method == 'POST':
        form = AbsenceEmployeForm(request.POST, request.FILES, instance=absence)
        if form.is_valid():
            form.save()
            return redirect('absences_list')
    else:
        form = AbsenceEmployeForm(instance=absence)
    return render(request, 'rh/absences/absence_form.html', {'form': form, 'action': 'Modifier'})

@login_required
@permission_required('rh.delete_absenceemploye', raise_exception=True)
def absence_delete(request, pk):
    absence = get_object_or_404(AbsenceEmploye, pk=pk)
    if request.method == 'POST':
        absence.delete()
        return redirect('absences_list')
    return render(request, 'rh/absences/absence_confirm_delete.html', {'absence': absence})

# --- TypeAbsence CRUD ---
@login_required
@permission_required('rh.add_typeabsence', raise_exception=True)
def typeabsence_create(request):
    if request.method == 'POST':
        form = TypeAbsenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('types_absence_list')
    else:
        form = TypeAbsenceForm()
    return render(request, 'rh/absences/typeabsence_form.html', {'form': form, 'action': 'Créer'})

@login_required
@permission_required('rh.change_typeabsence', raise_exception=True)
def typeabsence_update(request, pk):
    typeabsence = get_object_or_404(TypeAbsence, pk=pk)
    if request.method == 'POST':
        form = TypeAbsenceForm(request.POST, instance=typeabsence)
        if form.is_valid():
            form.save()
            return redirect('types_absence_list')
    else:
        form = TypeAbsenceForm(instance=typeabsence)
    return render(request, 'rh/absences/typeabsence_form.html', {'form': form, 'action': 'Modifier'})

@login_required
@permission_required('rh.delete_typeabsence', raise_exception=True)
def typeabsence_delete(request, pk):
    typeabsence = get_object_or_404(TypeAbsence, pk=pk)
    if request.method == 'POST':
        typeabsence.delete()
        return redirect('types_absence_list')
    return render(request, 'rh/absences/typeabsence_confirm_delete.html', {'typeabsence': typeabsence})

# --- DemandeConge CRUD ---
@login_required
@permission_required('rh.add_demandeconge', raise_exception=True)
def demandeconge_create(request):
    if request.method == 'POST':
        form = DemandeCongeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('demandes_conge_list')
    else:
        form = DemandeCongeForm()
    return render(request, 'rh/absences/demandeconge_form.html', {'form': form, 'action': 'Créer'})

@login_required
@permission_required('rh.change_demandeconge', raise_exception=True)
def demandeconge_update(request, pk):
    demande = get_object_or_404(DemandeConge, pk=pk)
    if request.method == 'POST':
        form = DemandeCongeForm(request.POST, instance=demande)
        if form.is_valid():
            form.save()
            return redirect('demandes_conge_list')
    else:
        form = DemandeCongeForm(instance=demande)
    return render(request, 'rh/absences/demandeconge_form.html', {'form': form, 'action': 'Modifier'})

@login_required
@permission_required('rh.delete_demandeconge', raise_exception=True)
def demandeconge_delete(request, pk):
    demande = get_object_or_404(DemandeConge, pk=pk)
    if request.method == 'POST':
        demande.delete()
        return redirect('demandes_conge_list')
    return render(request, 'rh/absences/demandeconge_confirm_delete.html', {'demande': demande})
