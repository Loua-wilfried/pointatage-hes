#!/usr/bin/env python
"""
Script pour créer automatiquement le superutilisateur Django
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hesfinance360.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    """Crée le superutilisateur avec les informations fournies"""
    
    username = 'Roland'
    email = 'rolandcarmel01@gmail.com'
    password = 'Caris@2@2@'
    
    try:
        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            print(f"❌ L'utilisateur '{username}' existe déjà!")
            user = User.objects.get(username=username)
            print(f"   Email: {user.email}")
            print(f"   Superutilisateur: {user.is_superuser}")
            return False
        
        # Créer le superutilisateur
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        print("✅ Superutilisateur créé avec succès!")
        print(f"   Nom d'utilisateur: {username}")
        print(f"   Email: {email}")
        print(f"   Statut: Superutilisateur")
        print(f"   ID: {user.id}")
        
        print("\n🔗 Vous pouvez maintenant vous connecter à:")
        print("   URL: http://127.0.0.1:8000/admin/")
        print(f"   Utilisateur: {username}")
        print("   Mot de passe: [celui que vous avez fourni]")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return False

if __name__ == "__main__":
    print("🔑 Création du superutilisateur Django")
    print("=" * 40)
    create_superuser()
