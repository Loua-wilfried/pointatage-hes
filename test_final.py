import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hesfinance360.settings')
django.setup()

import json
from django.test import Client
from django.contrib.auth.models import User

def test_api():
    client = Client()
    
    response = client.post('/api/register/', 
        data=json.dumps({
            'agence': 'finance360',
            'nom': 'Test User',
            'username': 'testuser777',
            'telephone': '0123456789',
            'email': 'testuser777@example.com',
            'password': 'Test123456',
            'confirmPassword': 'Test123456',
            'fonction': 'Administrateur système'
        }),
        content_type='application/json'
    )
    
    print('Status Code:', response.status_code)
    
    if response.status_code == 201:
        print('SUCCESS: API CORRIGÉE!')
        data = response.json()
        print('User:', data['user']['username'])
        print('Matricule:', data['employe']['matricule'])
        print('Token généré: OUI')
        
        # Nettoyage
        try:
            user = User.objects.get(username='testuser777')
            user.employe.delete()
            user.delete()
            print('Nettoyé')
        except:
            pass
        return True
    else:
        print('ERREUR PERSISTE')
        print('Contenu:', response.content.decode())
        return False

if __name__ == '__main__':
    success = test_api()
    print('RÉSULTAT FINAL:', 'SUCCÈS' if success else 'ÉCHEC')
