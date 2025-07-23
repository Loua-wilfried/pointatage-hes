#!/usr/bin/env python
"""
Script de test pour l'API d'enregistrement
"""
import os
import sys
import django
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hesfinance360.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from institutions.models import Employe
from roles_permissions.models import Role
from agences.models import Agence
import json

def test_register_api():
    """Test de l'API d'enregistrement"""
    print("=== TEST API REGISTER ===")
    
    # Vérifier les données disponibles
    print("\n1. Vérification des données disponibles:")
    agences = Agence.objects.all()[:3]
    roles = Role.objects.all()[:3]
    
    print(f"Agences disponibles ({agences.count()}):")
    for agence in agences:
        print(f"  - {agence.nom}")
    
    print(f"Rôles disponibles ({roles.count()}):")
    for role in roles:
        print(f"  - {role.nom_role}")
    
    if not agences.exists() or not roles.exists():
        print("❌ ERREUR: Pas d'agences ou de rôles disponibles")
        return False
    
    # Test de l'API
    print("\n2. Test de l'API d'enregistrement:")
    client = Client()
    
    test_data = {
        'agence': agences.first().nom,
        'nom': 'Test User API', 
        'username': 'testapi123',
        'telephone': '0123456789',
        'email': 'testapi@example.com',
        'password': 'Test123456',
        'confirmPassword': 'Test123456',
        'fonction': roles.first().nom_role
    }
    
    print(f"Données de test: {test_data}")
    
    try:
        response = client.post('/api/register/', 
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        print(f"\nRéponse API:")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            response_data = response.json()
            print("✅ SUCCESS: Compte créé avec succès!")
            print(f"Username: {response_data['user']['username']}")
            print(f"Matricule: {response_data['employe']['matricule']}")
            print(f"Agence: {response_data['employe']['agence']}")
            print(f"Fonction: {response_data['employe']['fonction']}")
            print(f"Token généré: {'access' in response_data['tokens']}")
            
            # Nettoyage
            try:
                user = User.objects.get(username='testapi123')
                employe = user.employe
                print(f"Employé trouvé: {employe.matricule_interne}")
                employe.delete()
                user.delete()
                print("🧹 Test nettoyé avec succès")
            except Exception as e:
                print(f"⚠️ Erreur lors du nettoyage: {e}")
            
            return True
            
        else:
            print("❌ ERREUR: Échec de la création")
            try:
                error_data = response.json()
                print(f"Détails: {error_data}")
            except:
                print(f"Contenu brut: {response.content.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_register_api()
    print(f"\n=== RÉSULTAT: {'✅ SUCCÈS' if success else '❌ ÉCHEC'} ===")
    sys.exit(0 if success else 1)
