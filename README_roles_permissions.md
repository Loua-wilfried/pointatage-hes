# Module Rôles & Permissions (Django)

## Installation

1. Ajouter `roles_permissions` dans `INSTALLED_APPS` de `settings.py`.
2. Lancer les migrations :
   ```bash
   python manage.py makemigrations roles_permissions
   python manage.py migrate
   ```
3. Accéder à l’admin Django pour gérer les rôles et permissions.
4. Protéger vos vues avec le décorateur `@permission_requise('code_permission')`.
5. Pour l’API REST, inclure `roles_permissions/urls.py` dans vos `urls.py` principaux.

## Exemple d’utilisation du décorateur

```python
from roles_permissions.decorators import permission_requise

@permission_requise('client_creer')
def vue_protegee(request):
    ...
```

## Exemple d’appel API

- `GET /roles/` → Liste des rôles
- `POST /roles/` → Créer un rôle
- `GET /permissions/` → Liste des permissions
- `POST /roles/{id}/permissions/` → Associer des permissions à un rôle

## Bonnes pratiques
- Attribuer les rôles via l’admin ou la fonction utilitaire `assignerRoleUtilisateur`.
- Ne jamais donner de permission directe à un utilisateur, toujours via un rôle.
- Utiliser le décorateur pour sécuriser les vues sensibles.
