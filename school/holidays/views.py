from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Holiday

@login_required(login_url='authentication:login')
def holiday_list(request):
    holidays = Holiday.objects.all()
    return render(request, 'holidays/holiday_list.html', {'holidays': holidays})

@login_required(login_url='authentication:login')
def add_holiday(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        description = request.POST.get('description')
        type_conge = request.POST.get('type_conge')
        
        if Holiday.objects.filter(name=name).exists():
            messages.error(request, 'Holiday with this name already exists!')
        else:
            Holiday.objects.create(
                name=name,
                date_debut=date_debut,
                date_fin=date_fin,
                description=description,
                type_conge=type_conge
            )
            messages.success(request, 'Holiday added successfully!')
            return redirect('holidays:holiday_list')
    
    return render(request, 'holidays/add_holiday.html')

@login_required(login_url='authentication:login')
def edit_holiday(request, holiday_id):
    holiday = get_object_or_404(Holiday, id=holiday_id)
    
    if request.method == 'POST':
        holiday.name = request.POST.get('name')
        holiday.date_debut = request.POST.get('date_debut')
        holiday.date_fin = request.POST.get('date_fin')
        holiday.description = request.POST.get('description')
        holiday.type_conge = request.POST.get('type_conge')
        holiday.save()
        messages.success(request, 'Holiday updated successfully!')
        return redirect('holidays:holiday_list')
    
    return render(request, 'holidays/edit_holiday.html', {'holiday': holiday})

@login_required(login_url='authentication:login')
def delete_holiday(request, holiday_id):
    holiday = get_object_or_404(Holiday, id=holiday_id)
    
    if request.method == 'POST':
        holiday.delete()
        messages.success(request, 'Holiday deleted successfully!')
        return redirect('holidays:holiday_list')
    
    return render(request, 'holidays/delete_holiday.html', {'holiday': holiday})
