from .models import Role, Permission, RolePermission, UserRole
from django.contrib.auth.models import User

def creerRole(nom, description, slug=None):
    return Role.objects.create(nom_role=nom, description=description, slug=slug)

def modifierRole(role_id, data):
    Role.objects.filter(id=role_id).update(**data)

def supprimerRole(role_id):
    Role.objects.filter(id=role_id).delete()

def listerRoles():
    return Role.objects.all()

def afficherPermissionsParRole(role_id):
    return Permission.objects.filter(rolepermission__role_id=role_id)

def creerPermission(nom_permission, description, module_associe):
    return Permission.objects.create(nom_permission=nom_permission, description=description, module_associe=module_associe)

def modifierPermission(permission_id, data):
    Permission.objects.filter(id=permission_id).update(**data)

def supprimerPermission(permission_id):
    Permission.objects.filter(id=permission_id).delete()

def attribuerPermission(role_id, permission_id):
    RolePermission.objects.get_or_create(role_id=role_id, permission_id=permission_id)

def retirerPermission(role_id, permission_id):
    RolePermission.objects.filter(role_id=role_id, permission_id=permission_id).delete()

def assignerRoleUtilisateur(user_id, role_id):
    user = User.objects.get(id=user_id)
    role = Role.objects.get(id=role_id)
    UserRole.objects.update_or_create(user=user, defaults={'role': role})

def verifierPermission(utilisateur_id, permission_code):
    try:
        user_role = UserRole.objects.get(user_id=utilisateur_id).role
        return Permission.objects.filter(rolepermission__role=user_role, nom_permission=permission_code).exists()
    except UserRole.DoesNotExist:
        return False

def getPermissionsUtilisateur(utilisateur_id):
    try:
        user_role = UserRole.objects.get(user_id=utilisateur_id).role
        return Permission.objects.filter(rolepermission__role=user_role)
    except UserRole.DoesNotExist:
        return Permission.objects.none()
