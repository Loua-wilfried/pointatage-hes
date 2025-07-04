from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Institution, PlanSaaS, Abonnement, Employe
from .forms import InstitutionForm, PlanSaaSForm, AbonnementForm
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta


def superadmin_required(user):
    return user.is_superuser

@method_decorator(user_passes_test(superadmin_required), name='dispatch')
class PlanSaaSListView(LoginRequiredMixin, ListView):
    model = PlanSaaS
    template_name = 'institutions/plan_list.html'
    context_object_name = 'plans'
    paginate_by = 10
    ordering = ['nom_plan']

@method_decorator(user_passes_test(superadmin_required), name='dispatch')
class PlanSaaSCreateView(LoginRequiredMixin, CreateView):
    model = PlanSaaS
    form_class = PlanSaaSForm
    template_name = 'clients/plan_form.html'
    success_url = reverse_lazy('plan_list')
    def form_valid(self, form):
        messages.success(self.request, "Plan créé avec succès.")
        return super().form_valid(form)

@method_decorator(user_passes_test(superadmin_required), name='dispatch')
class PlanSaaSUpdateView(LoginRequiredMixin, UpdateView):
    model = PlanSaaS
    form_class = PlanSaaSForm
    template_name = 'clients/plan_form.html'
    success_url = reverse_lazy('plan_list')
    def form_valid(self, form):
        messages.success(self.request, "Plan modifié avec succès.")
        return super().form_valid(form)

@method_decorator(user_passes_test(superadmin_required), name='dispatch')
class PlanSaaSDeleteView(LoginRequiredMixin, DeleteView):
    model = PlanSaaS
    template_name = 'institutions/plan_confirm_delete.html'
    success_url = reverse_lazy('plan_list')
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Plan supprimé avec succès.")
        return super().delete(request, *args, **kwargs)

@method_decorator(user_passes_test(superadmin_required), name='dispatch')
class AbonnementListView(LoginRequiredMixin, ListView):
    model = Abonnement
    template_name = 'institutions/abonnement_list.html'
    context_object_name = 'abonnements'
    paginate_by = 10
    ordering = ['-date_debut']

@method_decorator(user_passes_test(superadmin_required), name='dispatch')
class AbonnementCreateView(LoginRequiredMixin, CreateView):
    model = Abonnement
    form_class = AbonnementForm
    template_name = 'clients/abonnement_form.html'
    success_url = reverse_lazy('abonnement_list')
    def form_valid(self, form):
        messages.success(self.request, "Abonnement attribué avec succès.")
        return super().form_valid(form)

@method_decorator(user_passes_test(superadmin_required), name='dispatch')
class AbonnementUpdateView(LoginRequiredMixin, UpdateView):
    model = Abonnement
    form_class = AbonnementForm
    template_name = 'clients/abonnement_form.html'
    success_url = reverse_lazy('abonnement_list')
    def form_valid(self, form):
        messages.success(self.request, "Abonnement modifié avec succès.")
        return super().form_valid(form)

@method_decorator(user_passes_test(superadmin_required), name='dispatch')
class AbonnementDeleteView(LoginRequiredMixin, DeleteView):
    model = Abonnement
    template_name = 'institutions/abonnement_confirm_delete.html'
    success_url = reverse_lazy('abonnement_list')
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Abonnement supprimé avec succès.")
        return super().delete(request, *args, **kwargs)

# Actions métier : renouveler, suspendre, résilier
from django.views import View

@method_decorator(user_passes_test(superadmin_required), name='dispatch')
class AbonnementRenewView(LoginRequiredMixin, View):
    def post(self, request, pk):
        abo = get_object_or_404(Abonnement, pk=pk)
        # Prolonge de la même durée que l'abonnement initial
        duree = (abo.date_fin.year - abo.date_debut.year) * 12 + (abo.date_fin.month - abo.date_debut.month)
        if duree < 1:
            duree = 1
        # Calcule nouvelle date fin
        from datetime import date
        date_debut = abo.date_fin
        annee = date_debut.year + ((date_debut.month - 1 + duree) // 12)
        mois_final = ((date_debut.month - 1 + duree) % 12) + 1
        jour = min(date_debut.day, [31,29 if annee%4==0 and (annee%100!=0 or annee%400==0) else 28,31,30,31,30,31,31,30,31,30,31][mois_final-1])
        abo.date_debut = date_debut
        abo.date_fin = date(annee, mois_final, jour)
        abo.statut = 'actif'
        abo.save()
        messages.success(request, "Abonnement renouvelé.")
        return redirect('abonnement_list')

@method_decorator(user_passes_test(superadmin_required), name='dispatch')
class AbonnementSuspendView(LoginRequiredMixin, View):
    def post(self, request, pk):
        abo = get_object_or_404(Abonnement, pk=pk)
        abo.statut = 'suspendu'
        abo.save()
        messages.success(request, "Abonnement suspendu.")
        return redirect('abonnement_list')

@method_decorator(user_passes_test(superadmin_required), name='dispatch')
class AbonnementResilierView(LoginRequiredMixin, View):
    def post(self, request, pk):
        abo = get_object_or_404(Abonnement, pk=pk)
        abo.statut = 'termine'
        abo.save()
        messages.success(request, "Abonnement résilié.")
        return redirect('abonnement_list')

# Calcul de facture
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class EmployeListView(LoginRequiredMixin, ListView):
    model = Employe
    template_name = 'institutions/employe_list.html'
    context_object_name = 'employes'
    paginate_by = 20
    ordering = ['nom', 'prenom']

    def get_queryset(self):
        qs = super().get_queryset()
        role = self.request.GET.get('role')
        agence = self.request.GET.get('agence')
        statut = self.request.GET.get('statut')
        if role:
            qs = qs.filter(role_id=role)
        if agence:
            qs = qs.filter(agence_id=agence)
        if statut:
            qs = qs.filter(statut=statut)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roles'] = set(Employe.objects.values_list('role__id', 'role__nom_role'))
        context['agences'] = set(Employe.objects.values_list('agence__id', 'agence__nom'))
        context['statuts'] = Employe.STATUT_CHOICES
        return context


@user_passes_test(superadmin_required)
def calculer_facture(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        plan_id = data.get('plan_id')
        duree = int(data.get('duree', 1))
        plan = get_object_or_404(PlanSaaS, pk=plan_id)
        montant_total = float(plan.prix_mensuel) * duree
        return JsonResponse({'montant_total': montant_total})
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

class InstitutionListView(LoginRequiredMixin, ListView):
    model = Institution
    template_name = 'institutions/institution_list.html'
    context_object_name = 'institutions'
    paginate_by = 10
    ordering = ['-date_creation']

class InstitutionCreateView(LoginRequiredMixin, CreateView):
    model = Institution
    form_class = InstitutionForm
    template_name = 'clients/institution_form.html'
    success_url = reverse_lazy('institution_list')

    def form_valid(self, form):
        messages.success(self.request, "Institution créée avec succès.")
        return super().form_valid(form)

class InstitutionUpdateView(LoginRequiredMixin, UpdateView):
    model = Institution
    form_class = InstitutionForm
    template_name = 'clients/institution_form.html'
    success_url = reverse_lazy('institution_list')

    def form_valid(self, form):
        messages.success(self.request, "Institution modifiée avec succès.")
        return super().form_valid(form)

class InstitutionDeleteView(LoginRequiredMixin, DeleteView):
    model = Institution
    template_name = 'institutions/institution_confirm_delete.html'
    success_url = reverse_lazy('institution_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Institution supprimée avec succès.")
        return super().delete(request, *args, **kwargs)
