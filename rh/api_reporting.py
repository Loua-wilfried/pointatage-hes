from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rh.models import AbsenceEmploye, Pointage, Sanction
from institutions.models import Employe
from django.db.models import Count
from datetime import date, timedelta
import calendar

class ReportingRHAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        today = date.today()
        mois = today.month
        annee = today.year
        total_employes = Employe.objects.count()
        total_pointages = Pointage.objects.count()
        total_absences = AbsenceEmploye.objects.count()
        total_sanctions = Sanction.objects.count()
        absences_mois = AbsenceEmploye.objects.filter(date_debut__month=mois, date_debut__year=annee).count()
        sanctions_mois = Sanction.objects.filter(date__month=mois, date__year=annee).count()
        pointages_mois = Pointage.objects.filter(date__month=mois, date__year=annee).count()
        top_absents = list(AbsenceEmploye.objects.values('employe__nom', 'employe__prenom').annotate(total=Count('id')).order_by('-total')[:5])
        top_sanctionnes = list(Sanction.objects.values('employe__nom', 'employe__prenom').annotate(total=Count('id')).order_by('-total')[:5])
        # Données graphiques
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
            absences_data.append(AbsenceEmploye.objects.filter(date_debut__month=month, date_debut__year=year).count())
            sanctions_data.append(Sanction.objects.filter(date__month=month, date__year=year).count())
            pointages_data.append(Pointage.objects.filter(date__month=month, date__year=year).count())
        return Response({
            'total_employes': total_employes,
            'total_pointages': total_pointages,
            'total_absences': total_absences,
            'total_sanctions': total_sanctions,
            'absences_mois': absences_mois,
            'sanctions_mois': sanctions_mois,
            'pointages_mois': pointages_mois,
            'top_absents': top_absents,
            'top_sanctionnes': top_sanctionnes,
            'chart_labels': labels,
            'chart_absences': absences_data,
            'chart_sanctions': sanctions_data,
            'chart_pointages': pointages_data,
        })
