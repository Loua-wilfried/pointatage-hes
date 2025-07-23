import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hesfinance360.settings')
django.setup()

from roles_permissions.models import Role

# Récupérer tous les rôles
roles = Role.objects.all().order_by('id')

print("=== ROLES DANS LA BASE DE DONNEES ===")
for role in roles:
    print(f"ID: {role.id:2d} - {role.nom_role}")

print(f"\nTotal: {roles.count()} rôles")

print("\n=== CODE JAVASCRIPT POUR L'APP MOBILE ===")
print("const fonctions = [")
for role in roles:
    print(f'  {{ label: "{role.nom_role}", value: "{role.id}" }},')
print("];")

print("\n=== IDS DISPONIBLES ===")
ids = [role.id for role in roles]
print(f"IDs: {ids}")
print(f"Min ID: {min(ids)}, Max ID: {max(ids)}")
