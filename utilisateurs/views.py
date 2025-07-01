from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# Toutes les vues liées au modèle Utilisateur personnalisé ont été supprimées.
# Utilisez uniquement le modèle User natif de Django pour l'authentification et la gestion des utilisateurs.
@login_required
def profil_utilisateur(request):
    utilisateur = get_object_or_404(Utilisateur, user=request.user)
    return render(request, 'utilisateurs/profil.html', {'utilisateur': utilisateur})

@login_required
def activer_utilisateur(request, id):
    utilisateur = get_object_or_404(Utilisateur, id=id)
    utilisateur.statut_utilisateur = 'actif'
    utilisateur.save()
    utilisateur.user.is_active = True
    utilisateur.user.save()
    messages.success(request, 'Utilisateur activé.')
    return redirect('liste_utilisateurs')

@login_required
def desactiver_utilisateur(request, id):
    utilisateur = get_object_or_404(Utilisateur, id=id)
    utilisateur.statut_utilisateur = 'inactif'
    utilisateur.save()
    utilisateur.user.is_active = False
    utilisateur.user.save()
    messages.success(request, 'Utilisateur désactivé.')
    return redirect('liste_utilisateurs')
