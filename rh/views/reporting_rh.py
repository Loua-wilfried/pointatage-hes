from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from rh.models import AbsenceEmploye, Pointage, Sanction
from institutions.models import Employe
from django.db.models import Count, Sum
from datetime import date, timedelta
import calendar
import json
from rh.forms_reporting import ReportingRHFilterForm

@login_required
@permission_required('rh.view_pointage', raise_exception=True)
def reporting_rh(request):
    today = date.today()
    mois = today.month
    annee = today.year
    filter_form = ReportingRHFilterForm(request.GET or None)
    employe = None
    date_debut = None
    date_fin = None
    type_evenement = None
    if filter_form.is_valid():
        employe = filter_form.cleaned_data.get('employe')
        date_debut = filter_form.cleaned_data.get('date_debut')
        date_fin = filter_form.cleaned_data.get('date_fin')
        type_evenement = filter_form.cleaned_data.get('type_evenement')

    # Filtres dynamiques
    absences_qs = AbsenceEmploye.objects.all()
    sanctions_qs = Sanction.objects.all()
    pointages_qs = Pointage.objects.all()
    if employe:
        absences_qs = absences_qs.filter(employe=employe)
        sanctions_qs = sanctions_qs.filter(employe=employe)
        pointages_qs = pointages_qs.filter(employe=employe)
    if date_debut:
        absences_qs = absences_qs.filter(date_debut__gte=date_debut)
        sanctions_qs = sanctions_qs.filter(date__gte=date_debut)
        pointages_qs = pointages_qs.filter(date__gte=date_debut)
    if date_fin:
        absences_qs = absences_qs.filter(date_debut__lte=date_fin)
        sanctions_qs = sanctions_qs.filter(date__lte=date_fin)
        pointages_qs = pointages_qs.filter(date__lte=date_fin)

    # Statistiques globales filtrées
    total_employes = Employe.objects.count()
    total_pointages = pointages_qs.count()
    total_absences = absences_qs.count()
    total_sanctions = sanctions_qs.count()

    # Statistiques du mois en cours (filtrées)
    absences_mois = absences_qs.filter(date_debut__month=mois, date_debut__year=annee).count()
    sanctions_mois = sanctions_qs.filter(date__month=mois, date__year=annee).count()
    pointages_mois = pointages_qs.filter(date__month=mois, date__year=annee).count()

    # Top employés (filtrés)
    if not type_evenement or type_evenement == 'absence':
        top_absents = absences_qs.values('employe__nom', 'employe__prenom').annotate(total=Count('id')).order_by('-total')[:5]
    else:
        top_absents = []
    if not type_evenement or type_evenement == 'sanction':
        top_sanctionnes = sanctions_qs.values('employe__nom', 'employe__prenom').annotate(total=Count('id')).order_by('-total')[:5]
    else:
        top_sanctionnes = []

    # Données pour graphiques (12 derniers mois, filtrés)
    labels = []
    absences_data = []
    sanctions_data = []
    pointages_data = []
    for i in range(11, -1, -1):
        month_date = today.replace(day=1) - timedelta(days=30*i)
        month = month_date.month
        year = month_date.year
        label = f"{calendar.month_abbr[month]} {year}"
        labels.append(label)
        absences_data.append(absences_qs.filter(date_debut__month=month, date_debut__year=year).count())
        sanctions_data.append(sanctions_qs.filter(date__month=month, date__year=year).count())
        pointages_data.append(pointages_qs.filter(date__month=month, date__year=year).count())

    context = {
        'filter_form': filter_form,
        'total_employes': total_employes,
        'total_pointages': total_pointages,
        'total_absences': total_absences,
        'total_sanctions': total_sanctions,
        'absences_mois': absences_mois,
        'sanctions_mois': sanctions_mois,
        'pointages_mois': pointages_mois,
        'top_absents': top_absents,
        'top_sanctionnes': top_sanctionnes,
        'mois': mois,
        'annee': annee,
        'chart_labels': json.dumps(labels),
        'chart_absences': json.dumps(absences_data),
        'chart_sanctions': json.dumps(sanctions_data),
        'chart_pointages': json.dumps(pointages_data),
    }
    return render(request, 'rh/reporting/reporting_rh.html', context)
