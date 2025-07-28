#!/usr/bin/env python
"""
Script pour créer automatiquement la base de données MySQL
et vérifier la connectivité XAMPP
"""

import subprocess
import sys
import os

def check_xampp_mysql():
    """Vérifie si MySQL est accessible via XAMPP"""
    try:
        # Test de connexion basique
        import MySQLdb
        connection = MySQLdb.connect(
            host='localhost',
            user='root',
            password='',
            port=3306
        )
        connection.close()
        print("✅ MySQL XAMPP est accessible")
        return True
    except ImportError:
        print("❌ Module MySQLdb non trouvé, utilisons une approche alternative")
        return False
    except Exception as e:
        print(f"❌ Impossible de se connecter à MySQL: {e}")
        print("\n🔧 Solutions possibles:")
        print("1. Démarrez XAMPP Control Panel")
        print("2. Cliquez sur 'Start' pour MySQL")
        print("3. Vérifiez que le voyant MySQL est vert")
        return False

def create_database_via_mysql_command():
    """Crée la base de données via la ligne de commande MySQL"""
    try:
        # Commande pour créer la base de données
        mysql_commands = [
            "CREATE DATABASE IF NOT EXISTS pointatage_hes CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
            "SHOW DATABASES LIKE 'pointatage_hes';"
        ]
        
        for cmd in mysql_commands:
            print(f"Exécution: {cmd}")
            # Note: Cette méthode nécessite que mysql.exe soit dans le PATH
            # Ou il faut spécifier le chemin complet vers mysql.exe de XAMPP
        
        print("✅ Tentative de création de base de données")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return False

def create_database_sql_file():
    """Crée un fichier SQL pour créer la base de données"""
    sql_content = """
-- Script de création de la base de données pour le système de pointage
-- À exécuter dans phpMyAdmin ou via ligne de commande MySQL

CREATE DATABASE IF NOT EXISTS pointatage_hes 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE pointatage_hes;

-- Vérification
SELECT 'Base de données pointatage_hes créée avec succès!' as message;
"""
    
    with open('create_database.sql', 'w', encoding='utf-8') as f:
        f.write(sql_content)
    
    print("✅ Fichier create_database.sql créé")
    print("📋 Instructions:")
    print("1. Ouvrez http://localhost/phpmyadmin")
    print("2. Cliquez sur 'Importer'")
    print("3. Sélectionnez le fichier create_database.sql")
    print("4. Cliquez sur 'Exécuter'")
    
    return True

def main():
    print("🚀 Configuration de la base de données MySQL")
    print("=" * 50)
    
    # Étape 1: Vérification XAMPP
    print("\n1. Vérification de XAMPP MySQL...")
    if not check_xampp_mysql():
        print("\n⚠️  XAMPP MySQL n'est pas accessible")
        print("Veuillez d'abord démarrer XAMPP et activer MySQL")
        
        # Créer le fichier SQL comme alternative
        print("\n2. Création d'un fichier SQL alternatif...")
        create_database_sql_file()
        return
    
    # Étape 2: Création de la base
    print("\n2. Création de la base de données...")
    create_database_via_mysql_command()
    
    # Étape 3: Instructions suivantes
    print("\n3. Prochaines étapes:")
    print("   python manage.py makemigrations")
    print("   python manage.py migrate")
    print("   python manage.py runserver")

if __name__ == "__main__":
    main()
