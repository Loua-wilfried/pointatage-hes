import io
import pandas as pd
from django.db.models import Count
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from rh.models import AbsenceEmploye, Sanction
from institutions.models import Employe
from datetime import date
from django.shortcuts import redirect
from django.template.loader import render_to_string
from xhtml2pdf import pisa

@login_required
@permission_required('rh.view_pointage', raise_exception=True)
def export_top_absents_excel(request):
    data = AbsenceEmploye.objects.values('employe__nom', 'employe__prenom').annotate(total_absences=Count('id')).order_by('-total_absences')[:20]
    df = pd.DataFrame(list(data))
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Top Absents')
    output.seek(0)
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=top_absents.xlsx'
    return response

@login_required
@permission_required('rh.view_sanction', raise_exception=True)
def export_top_sanctionnes_excel(request):
    data = Sanction.objects.values('employe__nom', 'employe__prenom').annotate(total_sanctions=Count('id')).order_by('-total_sanctions')[:20]
    df = pd.DataFrame(list(data))
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Top Sanctionnés')
    output.seek(0)
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=top_sanctionnes.xlsx'
    return response

@login_required
@permission_required('rh.view_pointage', raise_exception=True)
def export_reporting_pdf(request):
    today = date.today()
    mois = today.month
    annee = today.year
    absences_mois = AbsenceEmploye.objects.filter(date_debut__month=mois, date_debut__year=annee).count()
    sanctions_mois = Sanction.objects.filter(date__month=mois, date__year=annee).count()
    top_absents = AbsenceEmploye.objects.values('employe__nom', 'employe__prenom').annotate(total=Count('id')).order_by('-total')[:5]
    top_sanctionnes = Sanction.objects.values('employe__nom', 'employe__prenom').annotate(total=Count('id')).order_by('-total')[:5]
    context = {
        'absences_mois': absences_mois,
        'sanctions_mois': sanctions_mois,
        'top_absents': top_absents,
        'top_sanctionnes': top_sanctionnes,
        'mois': mois,
        'annee': annee,
    }
    html = render_to_string('rh/reporting/reporting_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=reporting_rh.pdf'
    pisa.CreatePDF(io.StringIO(html), dest=response)
    return response
