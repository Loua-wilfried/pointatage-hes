from django import forms
from .models import Role, Permission, RolePermission

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['nom_role', 'description', 'slug']

class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['nom_permission', 'description', 'module_associe']

class RolePermissionForm(forms.ModelForm):
    class Meta:
        model = RolePermission
        fields = ['role', 'permission']
