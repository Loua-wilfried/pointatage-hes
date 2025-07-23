import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hesfinance360.settings')
django.setup()

import json
from django.test import Client
from roles_permissions.models import Role
from django.contrib.auth.models import User

def test_role_by_id():
    # Vérifier les rôles disponibles
    print('=== ROLES DISPONIBLES ===')
    for role in Role.objects.all()[:5]:
        print(f'ID: {role.id} - Nom: {role.nom_role}')
    
    # Test avec l'ID 14 (comme envoyé par l'app mobile)
    client = Client()
    test_data = {
        'agence': 'hesfinanceSA',
        'nom': 'Dago alex',
        'username': 'dago_test_id',
        'telephone': '0123456789',
        'email': 'dago_test@gmail.com',
        'password': 'Dago12345678',
        'confirmPassword': 'Dago12345678',
        'fonction': '14'  # ID du rôle comme envoyé par l'app
    }
    
    print('\n=== TEST AVEC ID ROLE 14 ===')
    response = client.post('/api/register/', 
        data=json.dumps(test_data),
        content_type='application/json'
    )
    
    print(f'Status Code: {response.status_code}')
    if response.status_code == 201:
        print('SUCCESS: Role trouve par ID!')
        data = response.json()
        print('User:', data['user']['username'])
        print('Matricule:', data['employe']['matricule'])
        print('Fonction:', data['employe']['fonction'])
        
        # Nettoyage
        try:
            user = User.objects.get(username='dago_test_id')
            user.employe.delete()
            user.delete()
            print('Nettoye')
        except:
            pass
        return True
    else:
        print('ERREUR:', response.content.decode())
        return False

if __name__ == '__main__':
    success = test_role_by_id()
    print('RESULTAT:', 'SUCCESS' if success else 'FAILED')
