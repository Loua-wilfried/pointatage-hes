#!/usr/bin/env python
"""
Script pour ajouter les rôles de développement à la base de données MySQL
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hesfinance360.settings')
django.setup()

from roles_permissions.models import Role

def add_developer_roles():
    """Ajoute les rôles de développement dans la base de données"""
    
    developer_roles = [
        {
            'nom_role': 'Développeur d\'application',
            'description': 'Conçoit, développe, teste et maintient les applications web, mobiles ou desktop utilisées par l\'institution. Il/elle travaille en collaboration avec les équipes métiers pour proposer des solutions performantes, sécurisées et évolutives.',
            'slug': 'developpeur-application'
        },
        {
            'nom_role': 'Assistant(e) Développeur d\'application',
            'description': 'Appuie le développeur principal dans l\'écriture du code, les tests, la correction de bugs, la documentation technique et la mise à jour des modules applicatifs.',
            'slug': 'assistant-developpeur-application'
        }
    ]
    
    created_count = 0
    updated_count = 0
    
    print("🚀 Ajout des rôles de développement")
    print("=" * 50)
    
    for role_data in developer_roles:
        try:
            # Vérifier si le rôle existe déjà
            role, created = Role.objects.get_or_create(
                slug=role_data['slug'],
                defaults={
                    'nom_role': role_data['nom_role'],
                    'description': role_data['description']
                }
            )
            
            if created:
                print(f"✅ Créé: {role_data['nom_role']}")
                created_count += 1
            else:
                # Mettre à jour si nécessaire
                if role.nom_role != role_data['nom_role'] or role.description != role_data['description']:
                    role.nom_role = role_data['nom_role']
                    role.description = role_data['description']
                    role.save()
                    print(f"🔄 Mis à jour: {role_data['nom_role']}")
                    updated_count += 1
                else:
                    print(f"⏭️  Existe déjà: {role_data['nom_role']}")
                    
        except Exception as e:
            print(f"❌ Erreur pour {role_data['nom_role']}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Résumé:")
    print(f"   ✅ Nouveaux rôles créés: {created_count}")
    print(f"   🔄 Rôles mis à jour: {updated_count}")
    print(f"   📈 Total rôles en base: {Role.objects.count()}")
    
    print("\n🎯 Secteur IT & Développement maintenant complet:")
    it_roles = Role.objects.filter(slug__in=[
        'responsable-it', 'assistant-responsable-it',
        'administrateur-bdd', 'assistant-administrateur-bdd',
        'administrateur-systeme',
        'securite-informatique', 'assistant-securite-informatique',
        'developpeur-application', 'assistant-developpeur-application'
    ])
    
    for role in it_roles:
        print(f"   - {role.nom_role}")
    
    print(f"\n📋 Total rôles IT: {it_roles.count()}")
    print("\n🔗 Voir dans l'admin Django:")
    print("   http://127.0.0.1:8000/admin/roles_permissions/role/")

if __name__ == "__main__":
    add_developer_roles()
