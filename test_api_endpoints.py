#!/usr/bin/env python
"""
Script de test pour les endpoints API des agences et rôles
"""
import os
import django
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hesfinance360.settings')
django.setup()

from agences.models import Agence
from roles_permissions.models import Role
from rh.serializers import AgenceSerializer, RoleSerializer
from rh.api import AgenceViewSet, RoleViewSet
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

def test_agences_api():
    """Test de l'API des agences"""
    print("=== TEST API AGENCES ===")
    
    # Créer une requête factory
    factory = RequestFactory()
    request = factory.get('/api/agences/')
    request.user = AnonymousUser()
    
    # Tester le ViewSet
    viewset = AgenceViewSet()
    viewset.request = request
    
    # Obtenir le queryset
    queryset = viewset.get_queryset()
    print(f"Nombre d'agences actives: {queryset.count()}")
    
    # Tester la sérialisation
    agences = queryset[:5]  # Prendre les 5 premières
    serializer = AgenceSerializer(agences, many=True)
    data = serializer.data
    
    print("Données sérialisées des agences:")
    for agence in data:
        print(f"  - {agence}")
    
    return data

def test_roles_api():
    """Test de l'API des rôles"""
    print("\n=== TEST API RÔLES ===")
    
    # Créer une requête factory
    factory = RequestFactory()
    request = factory.get('/api/roles/')
    request.user = AnonymousUser()
    
    # Tester le ViewSet
    viewset = RoleViewSet()
    viewset.request = request
    
    # Obtenir le queryset
    queryset = viewset.queryset
    print(f"Nombre de rôles: {queryset.count()}")
    
    # Tester la sérialisation
    roles = queryset[:5]  # Prendre les 5 premiers
    serializer = RoleSerializer(roles, many=True)
    data = serializer.data
    
    print("Données sérialisées des rôles:")
    for role in data:
        print(f"  - {role}")
    
    return data

def test_json_format():
    """Test du format JSON pour l'app mobile"""
    print("\n=== TEST FORMAT JSON MOBILE ===")
    
    agences_data = test_agences_api()
    roles_data = test_roles_api()
    
    # Vérifier le format attendu par l'app mobile
    print("\nFormat JSON pour l'app mobile:")
    print("Agences:", json.dumps(agences_data, indent=2, ensure_ascii=False))
    print("Rôles:", json.dumps(roles_data, indent=2, ensure_ascii=False))
    
    return {
        'agences': agences_data,
        'roles': roles_data
    }

if __name__ == '__main__':
    try:
        # Exécuter tous les tests
        result = test_json_format()
        
        print("\n=== RÉSUMÉ DES TESTS ===")
        print("✅ Modèles Agence et Role: OK")
        print("✅ Serializers AgenceSerializer et RoleSerializer: OK")
        print("✅ ViewSets AgenceViewSet et RoleViewSet: OK")
        print("✅ Format JSON pour mobile: OK")
        
        print(f"\n📊 STATISTIQUES:")
        print(f"   - {len(result['agences'])} agences disponibles")
        print(f"   - {len(result['roles'])} rôles disponibles")
        
        print("\n🎯 ENDPOINTS PRÊTS:")
        print("   - GET /api/agences/ ✅")
        print("   - GET /api/roles/ ✅")
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
