#!/usr/bin/env python
"""
Script de debug pour tester l'endpoint register sans passer par l'API
"""
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hesfinance360.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction
from institutions.models import Employe
from agences.models import Agence
from roles_permissions.models import Role
from rh.views_api_auth import generate_matricule
from datetime import date
import traceback

User = get_user_model()

def test_register_logic():
    """Test de la logique de création de compte"""
    print("=== DEBUG REGISTER LOGIC ===")
    
    # Données de test identiques à celles de l'app mobile
    data = {
        'agence': '0001',
        'nom': 'ROLAND CARMEL',
        'username': 'debug_test',
        'telephone': '0777999999',
        'email': 'debug_test@test.com',
        'password': '1234',
        'confirmPassword': '1234',
        'fonction': 1
    }
    
    try:
        print(f"1. Données reçues: {data}")
        
        # Extraction des données comme dans l'endpoint
        agence_id = data.get('agence')
        nom_complet = data.get('nom', '').strip()
        username = data.get('username', '').strip().lower()
        telephone = data.get('telephone', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        fonction_id = data.get('fonction')
        
        print(f"2. Données extraites:")
        print(f"   agence_id: '{agence_id}' (type: {type(agence_id)})")
        print(f"   nom_complet: '{nom_complet}' (type: {type(nom_complet)})")
        print(f"   username: '{username}' (type: {type(username)})")
        print(f"   email: '{email}' (type: {type(email)})")
        print(f"   fonction_id: '{fonction_id}' (type: {type(fonction_id)})")
        
        # Récupération des objets de référence
        print(f"3. Récupération agence avec ID '{agence_id}'...")
        agence = Agence.objects.get(id=agence_id)
        print(f"   Agence trouvée: {agence.nom}")
        
        print(f"4. Récupération rôle avec ID '{fonction_id}'...")
        if str(fonction_id).isdigit():
            role = Role.objects.get(id=int(fonction_id))
        else:
            role = Role.objects.get(nom_role=fonction_id)
        print(f"   Rôle trouvé: {role.nom_role}")
        
        # Vérifications d'unicité
        print("5. Vérifications d'unicité...")
        if User.objects.filter(username=username).exists():
            print(f"   ❌ Username '{username}' déjà utilisé")
            return False
        if User.objects.filter(email=email).exists():
            print(f"   ❌ Email '{email}' déjà utilisé")
            return False
        if Employe.objects.filter(telephone=telephone).exists():
            print(f"   ❌ Téléphone '{telephone}' déjà utilisé")
            return False
        print("   ✅ Toutes les vérifications d'unicité passent")
        
        # Transaction atomique
        print("6. Début de la transaction atomique...")
        with transaction.atomic():
            # Création du User
            print("7. Création du User Django...")
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=nom_complet.split()[0],
                last_name=' '.join(nom_complet.split()[1:]) if len(nom_complet.split()) > 1 else ''
            )
            print(f"   User créé: {user.username} (ID: {user.id})")
            
            # Séparation du nom
            nom_parts = nom_complet.split()
            prenom = nom_parts[0]
            nom_famille = ' '.join(nom_parts[1:]) if len(nom_parts) > 1 else prenom
            print(f"8. Nom séparé: prenom='{prenom}', nom='{nom_famille}'")
            
            # Génération matricule
            print("9. Génération du matricule...")
            matricule = generate_matricule()
            print(f"   Matricule généré: {matricule}")
            
            # Création de l'Employé
            print("10. Création de l'Employé...")
            employe = Employe.objects.create(
                user=user,
                nom=nom_famille,
                prenom=prenom,
                email=email,
                telephone=telephone,
                agence=agence,
                role=role,
                matricule_interne=matricule,
                sexe='M',
                date_naissance=date(1990, 1, 1),
                lieu_naissance='À compléter',
                nationalite='Ivoirienne',
                situation_familiale='celibataire',
                adresse='À compléter par le DRH',
                numero_cni='À compléter',
                date_embauche=date.today(),
                type_contrat='CDI',
                horaire_travail='08h00-17h00',
                salaire_base=0.00,
                rib_banque='À compléter',
                statut='actif'
            )
            print(f"   Employé créé: ID={employe.id}, Matricule={employe.matricule_interne}")
            
        print("11. Transaction terminée avec succès")
        print(f"✅ SUCCÈS - Compte créé pour {nom_complet}")
        
        # Nettoyage
        employe.delete()
        user.delete()
        print("12. Nettoyage effectué")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {type(e).__name__}: {str(e)}")
        print("Traceback complet:")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = test_register_logic()
    if success:
        print("\n🎉 Le test de création de compte a réussi!")
        print("Le problème ne vient PAS de la logique de création.")
        print("Il faut chercher dans la gestion des requêtes HTTP ou DRF.")
    else:
        print("\n💥 Le test de création de compte a échoué!")
        print("Le problème vient de la logique de création elle-même.")
