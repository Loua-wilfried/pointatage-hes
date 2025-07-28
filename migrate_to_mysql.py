#!/usr/bin/env python
"""
Script de migration vers MySQL/XAMPP
Ce script aide à configurer la base de données MySQL pour le projet Django
"""

import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line

def create_mysql_settings():
    """Crée la configuration MySQL pour settings.py"""
    mysql_config = '''
# Configuration MySQL pour XAMPP
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pointatage_hes',
        'USER': 'root',
        'PASSWORD': '',  # Par défaut XAMPP n'a pas de mot de passe
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
'''
    return mysql_config

def backup_current_settings():
    """Sauvegarde le fichier settings.py actuel"""
    settings_path = 'hesfinance360/settings.py'
    backup_path = 'hesfinance360/settings_sqlite_backup.py'
    
    if os.path.exists(settings_path):
        with open(settings_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Sauvegarde créée: {backup_path}")
        return True
    return False

def main():
    print("🚀 Script de migration vers MySQL/XAMPP")
    print("=" * 50)
    
    # Étape 1: Sauvegarde
    print("1. Sauvegarde du fichier settings.py...")
    if backup_current_settings():
        print("   ✅ Sauvegarde réussie")
    else:
        print("   ❌ Erreur lors de la sauvegarde")
        return
    
    # Étape 2: Affichage de la configuration MySQL
    print("\n2. Configuration MySQL à ajouter:")
    print("-" * 30)
    print(create_mysql_settings())
    
    print("\n3. Instructions suivantes:")
    print("   - Démarrez XAMPP et activez MySQL")
    print("   - Créez une base de données 'pointatage_hes' via phpMyAdmin")
    print("   - Modifiez settings.py avec la configuration MySQL ci-dessus")
    print("   - Exécutez: python manage.py makemigrations")
    print("   - Exécutez: python manage.py migrate")

if __name__ == "__main__":
    main()
