from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Agence
from .forms import AgenceForm
from institutions.models import Institution
from django.core.paginator import Paginator

@login_required
def liste_agences(request):
    user = request.user
    agences = Agence.objects.all()
    # Filtrage par institution si restriction utilisateur
    if hasattr(user, 'institution'):
        agences = agences.filter(institution=user.institution)
    paginator = Paginator(agences, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'agences/agence_list.html', {'page_obj': page_obj})

@login_required
def creer_agence(request):
    if request.method == 'POST':
        form = AgenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_agences')
    else:
        form = AgenceForm()
    return render(request, 'agences/agence_form.html', {'form': form})

@login_required
def modifier_agence(request, id):
    agence = get_object_or_404(Agence, id=id)
    if request.method == 'POST':
        form = AgenceForm(request.POST, instance=agence)
        if form.is_valid():
            form.save()
            return redirect('liste_agences')
    else:
        form = AgenceForm(instance=agence)
    return render(request, 'agences/agence_form.html', {'form': form, 'agence': agence})

@login_required
def supprimer_agence(request, id):
    agence = get_object_or_404(Agence, id=id)
    if request.method == 'POST':
        agence.delete()
        return redirect('liste_agences')
    return render(request, 'agences/agence_confirm_delete.html', {'agence': agence})
