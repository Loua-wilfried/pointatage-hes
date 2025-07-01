from django.shortcuts import render, redirect, get_object_or_404

def home(request):
    return render(request, 'roles_permissions/home.html')

from django.contrib import messages
from .models import Role, Permission, RolePermission
from .forms import RoleForm, PermissionForm, RolePermissionForm
from django.views.decorators.csrf import csrf_exempt
from .models import UserRole

def roles_list(request):
    roles = Role.objects.all()
    return render(request, 'roles_permissions/roles_list.html', {'roles': roles})

def role_create(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rôle créé avec succès.')
            return redirect('roles_list')
    else:
        form = RoleForm()
    return render(request, 'roles_permissions/role_form.html', {'form': form})

def role_edit(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rôle modifié avec succès.')
            return redirect('roles_list')
    else:
        form = RoleForm(instance=role)
    return render(request, 'roles_permissions/role_form.html', {'form': form})

def role_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        role.delete()
        messages.success(request, 'Rôle supprimé.')
        return redirect('roles_list')
    return render(request, 'roles_permissions/confirm_delete.html', {'object': role, 'type': 'rôle', 'cancel_url': 'roles_list'})

def permissions_list(request):
    permissions = Permission.objects.all()
    return render(request, 'roles_permissions/permissions_list.html', {'permissions': permissions})

def permission_create(request):
    if request.method == 'POST':
        form = PermissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Permission créée avec succès.')
            return redirect('permissions_list')
    else:
        form = PermissionForm()
    return render(request, 'roles_permissions/permission_form.html', {'form': form})

def permission_edit(request, pk):
    permission = get_object_or_404(Permission, pk=pk)
    if request.method == 'POST':
        form = PermissionForm(request.POST, instance=permission)
        if form.is_valid():
            form.save()
            messages.success(request, 'Permission modifiée avec succès.')
            return redirect('permissions_list')
    else:
        form = PermissionForm(instance=permission)
    return render(request, 'roles_permissions/permission_form.html', {'form': form})

def permission_delete(request, pk):
    permission = get_object_or_404(Permission, pk=pk)
    if request.method == 'POST':
        permission.delete()
        messages.success(request, 'Permission supprimée.')
        return redirect('permissions_list')
    return render(request, 'roles_permissions/confirm_delete.html', {'object': permission, 'type': 'permission', 'cancel_url': 'permissions_list'})

def affectations_list(request):
    affectations = RolePermission.objects.select_related('role', 'permission')
    return render(request, 'roles_permissions/affectations_list.html', {'affectations': affectations})

def affectation_create(request):
    if request.method == 'POST':
        form = RolePermissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Affectation créée.')
            return redirect('affectations_list')
    else:
        form = RolePermissionForm()
    return render(request, 'roles_permissions/affectation_form.html', {'form': form})

def affectation_delete(request, pk):
    affectation = get_object_or_404(RolePermission, pk=pk)
    if request.method == 'POST':
        affectation.delete()
        messages.success(request, 'Affectation supprimée.')
        return redirect('affectations_list')
    return render(request, 'roles_permissions/confirm_delete.html', {'object': affectation, 'type': 'affectation', 'cancel_url': 'affectations_list'})

def affectation_visuelle(request):
    from collections import defaultdict
    roles = Role.objects.all()
    permissions = Permission.objects.all()
    selected_role_id = int(request.POST.get('role', roles.first().id if roles else 0)) if request.method == 'POST' else int(request.GET.get('role', roles.first().id if roles else 0))
    assigned_permissions = set(RolePermission.objects.filter(role_id=selected_role_id).values_list('permission_id', flat=True))
    permissions_by_module = defaultdict(list)
    for perm in permissions:
        permissions_by_module[perm.module_associe].append(perm)
    if request.method == 'POST':
        checked_permissions = set(map(int, request.POST.getlist('permissions')))
        # Ajout des permissions cochées
        for perm in checked_permissions - assigned_permissions:
            RolePermission.objects.create(role_id=selected_role_id, permission_id=perm)
        # Suppression des permissions décochées
        for perm in assigned_permissions - checked_permissions:
            RolePermission.objects.filter(role_id=selected_role_id, permission_id=perm).delete()
        messages.success(request, 'Affectations mises à jour.')
        assigned_permissions = checked_permissions
    return render(request, 'roles_permissions/affectation_visuelle.html', {
        'roles': roles,
        'permissions_by_module': permissions_by_module,
        'selected_role_id': selected_role_id,
        'assigned_permissions': assigned_permissions
    })

def userroles_list(request):
    userroles = UserRole.objects.select_related('user', 'role').all()
    return render(request, 'roles_permissions/userroles_list.html', {'userroles': userroles})
