from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Role, Permission, RolePermission
from .serializers import RoleSerializer, PermissionSerializer, RolePermissionSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import RoleForm

# API ViewSets
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    @action(detail=True, methods=['get'])
    def permissions(self, request, pk=None):
        role = self.get_object()
        permissions = Permission.objects.filter(rolepermission__role=role)
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer

# HTML CRUD views for Role
@login_required
def role_list(request):
    roles = Role.objects.all()
    return render(request, 'roles_permissions/role_list.html', {'roles': roles})

@login_required
def role_create(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('role_list')
    else:
        form = RoleForm()
    return render(request, 'roles_permissions/role_form.html', {'form': form})

@login_required
def role_update(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('role_list')
    else:
        form = RoleForm(instance=role)
    return render(request, 'roles_permissions/role_form.html', {'form': form, 'role': role})

@login_required
def role_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        role.delete()
        return redirect('role_list')
    return render(request, 'roles_permissions/role_confirm_delete.html', {'role': role})
