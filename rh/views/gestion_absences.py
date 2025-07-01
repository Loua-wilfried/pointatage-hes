from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from rh.models import AbsenceEmploye, TypeAbsence, DemandeConge

@login_required
@permission_required('rh.view_absenceemploye', raise_exception=True)
def absences_list(request):
    absences = AbsenceEmploye.objects.select_related('employe', 'type_absence').all()
    return render(request, 'rh/absences/absences_list.html', {'absences': absences})

@login_required
@permission_required('rh.view_typeabsence', raise_exception=True)
def types_absence_list(request):
    types = TypeAbsence.objects.all()
    return render(request, 'rh/absences/types_absence_list.html', {'types_absence': types})

@login_required
@permission_required('rh.view_demandeconge', raise_exception=True)
def demandes_conge_list(request):
    demandes = DemandeConge.objects.select_related('employe', 'type_absence').all()
    return render(request, 'rh/absences/demandes_conge_list.html', {'demandes_conge': demandes})
