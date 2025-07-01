from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    nom_role = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.nom_role

class Permission(models.Model):
    nom_permission = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    module_associe = models.CharField(max_length=100)

    def __str__(self):
        return self.nom_permission

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'permission')

class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
