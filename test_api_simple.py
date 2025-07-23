#!/usr/bin/env python
import os
import django
import sys

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hesfinance360.settings')
django.setup()

import json
from django.test import Client
from django.contrib.auth.models import User
from institutions.models import Employe

def test_api():
    client = Client()
    
    test_data = {
        'agence': 'finance360',
        'nom': 'Test User Final',
        'username': 'testuserfinal',
        'telephone': '0123456789',
        'email': 'testuserfinal@example.com',
        'password': 'Test123456',
        'confirmPassword': 'Test123456',
        'fonction': 'Administrateur système'
    }
    
    print('=== TEST API REGISTER ===')
    print('Données:', test_data)
    
    response = client.post('/api/register/', 
        data=json.dumps(test_data),
        content_type='application/json'
    )
    
    print('Status Code:', response.status_code)
    
    if response.status_code == 201:
        print('SUCCESS: API fonctionne!')
        data = response.json()
        print('User:', data['user']['username'])
        print('Matricule:', data['employe']['matricule'])
        
        # Nettoyage
        try:
            user = User.objects.get(username='testuserfinal')
            user.employe.delete()
            user.delete()
            print('Nettoyé')
        except:
            pass
        return True
    else:
        print('ERREUR')
        try:
            print('Réponse:', response.json())
        except:
            print('Contenu:', response.content.decode())
        return False

if __name__ == '__main__':
    success = test_api()
    print('RÉSULTAT:', 'SUCCESS' if success else 'FAILED')
