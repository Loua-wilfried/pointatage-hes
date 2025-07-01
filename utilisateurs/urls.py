from django.urls import path
from . import views

urlpatterns = [
    # URLs : Utilisez uniquement les routes liées à l'authentification Django si besoin.'', views.liste_utilisateurs, name='liste_utilisateurs'),
    # URLs : Utilisez uniquement les routes liées à l'authentification Django si besoin.'nouveau/', views.creer_utilisateur, name='creer_utilisateur'),
    # URLs : Utilisez uniquement les routes liées à l'authentification Django si besoin.'modifier/<int:id>/', views.modifier_utilisateur, name='modifier_utilisateur'),
    # URLs : Utilisez uniquement les routes liées à l'authentification Django si besoin.'supprimer/<int:id>/', views.supprimer_utilisateur, name='supprimer_utilisateur'),
    # URLs : Utilisez uniquement les routes liées à l'authentification Django si besoin.'changer-mdp/<int:id>/', views.changer_mot_de_passe, name='changer_mot_de_passe'),
    # URLs : Utilisez uniquement les routes liées à l'authentification Django si besoin.'attribuer-role/<int:id>/', views.attribuer_role, name='attribuer_role'),
    # URLs : Utilisez uniquement les routes liées à l'authentification Django si besoin.'profil/', views.profil_utilisateur, name='profil_utilisateur'),
    # URLs : Utilisez uniquement les routes liées à l'authentification Django si besoin.'activer/<int:id>/', views.activer_utilisateur, name='activer_utilisateur'),
    # URLs : Utilisez uniquement les routes liées à l'authentification Django si besoin.'desactiver/<int:id>/', views.desactiver_utilisateur, name='desactiver_utilisateur'),
    # URLs : Utilisez uniquement les routes liées à l'authentification Django si besoin.'login/', views.connexion, name='connexion'),
    # URLs : Utilisez uniquement les routes liées à l'authentification Django si besoin.'logout/', views.deconnexion, name='deconnexion'),
]
