from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from rh.models import Sanction
from rh.forms import SanctionForm

@login_required
@permission_required('rh.view_sanction', raise_exception=True)
def sanctions_list(request):
    sanctions = Sanction.objects.select_related('employe').order_by('-date', '-created_at')
    return render(request, 'rh/sanctions/sanctions_list.html', {'sanctions': sanctions})

@login_required
@permission_required('rh.add_sanction', raise_exception=True)
def sanction_create(request):
    if request.method == 'POST':
        form = SanctionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('sanctions_list')
    else:
        form = SanctionForm()
    return render(request, 'rh/sanctions/sanction_form.html', {'form': form})

@login_required
@permission_required('rh.change_sanction', raise_exception=True)
def sanction_update(request, pk):
    sanction = get_object_or_404(Sanction, pk=pk)
    if request.method == 'POST':
        form = SanctionForm(request.POST, request.FILES, instance=sanction)
        if form.is_valid():
            form.save()
            return redirect('sanctions_list')
    else:
        form = SanctionForm(instance=sanction)
    return render(request, 'rh/sanctions/sanction_form.html', {'form': form, 'sanction': sanction})

@login_required
@permission_required('rh.delete_sanction', raise_exception=True)
def sanction_delete(request, pk):
    sanction = get_object_or_404(Sanction, pk=pk)
    if request.method == 'POST':
        sanction.delete()
        return redirect('sanctions_list')
    return render(request, 'rh/sanctions/sanction_confirm_delete.html', {'sanction': sanction})
