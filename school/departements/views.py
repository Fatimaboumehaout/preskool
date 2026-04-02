from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Departement

@login_required(login_url='authentication:login')
def departement_list(request):
    departements = Departement.objects.all()
    return render(request, 'departements/departement_list.html', {'departements': departements})

@login_required(login_url='authentication:login')
def add_departement(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if Departement.objects.filter(name=name).exists():
            messages.error(request, 'Departement with this name already exists!')
        else:
            Departement.objects.create(
                name=name,
                description=description
            )
            messages.success(request, 'Departement added successfully!')
            return redirect('departements:departement_list')
    
    return render(request, 'departements/add_departement.html')

@login_required(login_url='authentication:login')
def edit_departement(request, departement_id):
    departement = get_object_or_404(Departement, id=departement_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if Departement.objects.filter(name=name).exclude(id=departement_id).exists():
            messages.error(request, 'Departement with this name already exists!')
        else:
            departement.name = name
            departement.description = description
            departement.save()
            messages.success(request, 'Departement updated successfully!')
            return redirect('departements:departement_list')
    
    return render(request, 'departements/edit_departement.html', {'departement': departement})

@login_required(login_url='authentication:login')
def delete_departement(request, departement_id):
    departement = get_object_or_404(Departement, id=departement_id)
    
    if request.method == 'POST':
        departement.delete()
        messages.success(request, 'Departement deleted successfully!')
        return redirect('departements:departement_list')
    
    return render(request, 'departements/delete_departement.html', {'departement': departement})
