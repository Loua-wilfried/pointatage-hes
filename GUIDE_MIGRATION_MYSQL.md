# 🚀 Guide de Migration vers MySQL/XAMPP

## ✅ Étapes déjà réalisées

1. **Installation du connecteur MySQL** : `mysqlclient` installé avec succès
2. **Sauvegarde de settings.py** : Fichier sauvegardé dans `hesfinance360/settings_sqlite_backup.py`
3. **Configuration MySQL** : `settings.py` mis à jour pour utiliser MySQL

## 📋 Étapes à suivre maintenant

### **Étape 1 : Démarrer XAMPP**

1. Lancez XAMPP Control Panel
2. Démarrez les services **Apache** et **MySQL**
3. Vérifiez que MySQL fonctionne (voyant vert)

### **Étape 2 : Créer la base de données**

1. Ouvrez votre navigateur
2. Allez sur `http://localhost/phpmyadmin`
3. Cliquez sur "Nouvelle base de données"
4. Nom de la base : `pointatage_hes`
5. Collation : `utf8mb4_unicode_ci`
6. Cliquez sur "Créer"

### **Étape 3 : Appliquer les migrations Django**

Exécutez ces commandes dans l'ordre :

```bash
# 1. Créer les nouvelles migrations
python manage.py makemigrations

# 2. Appliquer les migrations sur MySQL
python manage.py migrate

# 3. Créer un superutilisateur (optionnel)
python manage.py createsuperuser
```

### **Étape 4 : Tester la migration**

```bash
# Démarrer le serveur de développement
python manage.py runserver

# Vérifier que l'application fonctionne
# Ouvrir http://127.0.0.1:8000 dans le navigateur
```

## 🔧 Configuration MySQL actuelle

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pointatage_hes',
        'USER': 'root',
        'PASSWORD': '',  # Par défaut XAMPP
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

## 🚨 Problèmes potentiels et solutions

### **Erreur : "Access denied for user 'root'"**
- Vérifiez que MySQL est démarré dans XAMPP
- Vérifiez le mot de passe (par défaut vide dans XAMPP)

### **Erreur : "Can't connect to MySQL server"**
- Vérifiez que le port 3306 n'est pas bloqué
- Redémarrez MySQL dans XAMPP

### **Erreur de migration**
- Supprimez les fichiers de migration dans chaque app
- Recréez les migrations : `python manage.py makemigrations`

## 📊 Récupération des données (si nécessaire)

Si vous avez des données importantes dans SQLite :

1. **Nettoyage des données avec caractères spéciaux** :
```python
# Script pour nettoyer les emojis/caractères spéciaux
python manage.py shell
>>> from rh.models import *
>>> # Nettoyer les données problématiques
```

2. **Export sélectif** :
```bash
# Exporter seulement certaines tables
python manage.py dumpdata institutions.employe --output=employes.json
python manage.py dumpdata rh.demandeconge --output=demandes.json
```

3. **Import dans MySQL** :
```bash
# Après migration MySQL
python manage.py loaddata employes.json
python manage.py loaddata demandes.json
```

## 🎯 Vérifications finales

- [ ] XAMPP MySQL démarré
- [ ] Base de données `pointatage_hes` créée
- [ ] Migrations appliquées sans erreur
- [ ] Application accessible via navigateur
- [ ] Connexion admin fonctionnelle

## 📞 Support

En cas de problème, vérifiez :
1. Les logs de XAMPP
2. Les logs Django dans le terminal
3. La connectivité MySQL via phpMyAdmin
