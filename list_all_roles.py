#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hesfinance360.settings')
django.setup()

from roles_permissions.models import Role

def main():
    print("=== LISTE COMPLETE DES ROLES ===")
    roles = Role.objects.all().order_by('id')
    
    for role in roles:
        print(f"ID: {role.id:2d} | Nom: '{role.nom_role}'")
    
    print(f"\nTotal: {roles.count()} rôles")
    print(f"IDs disponibles: {list(roles.values_list('id', flat=True))}")
    
    # Générer le code JavaScript pour l'app mobile
    print("\n=== CODE POUR L'APP MOBILE ===")
    print("const fonctions = [")
    for role in roles:
        print(f"  {{ label: '{role.nom_role}', value: '{role.id}' }},")
    print("];")

if __name__ == '__main__':
    main()
