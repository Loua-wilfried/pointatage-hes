import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hesfinance360.settings')
django.setup()

from roles_permissions.models import Role

print('=== TOUS LES ROLES DISPONIBLES ===')
roles = Role.objects.all().order_by('id')
for role in roles:
    print(f'ID: {role.id:2d} - Nom: "{role.nom_role}"')

print(f'\nTotal: {roles.count()} rôles')
print(f'IDs disponibles: {[role.id for role in roles]}')
