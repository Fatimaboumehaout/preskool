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
        date = request.POST.get('date')  # Le template envoie 'date'
        description = request.POST.get('description')
        holiday_type = request.POST.get('holiday_type')  # Le template envoie 'holiday_type'
        
        # Validation simple
        if not name or not date:
            messages.error(request, 'Le nom et la date sont obligatoires!')
            return render(request, 'holidays/add_holiday.html')
        
        if Holiday.objects.filter(name=name).exists():
            messages.error(request, 'Une vacance avec ce nom existe déjà!')
            return render(request, 'holidays/add_holiday.html')
        else:
            holiday = Holiday.objects.create(
                name=name,
                date_debut=date,  # Utiliser date comme date_debut
                date_fin=date,    # Utiliser date comme date_fin pour l'instant
                description=description,
                type_conge=holiday_type
            )
            messages.success(request, 'Vacance ajoutée avec succès!')
            return render(request, 'holidays/holiday_success.html', {'holiday': holiday})
    
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
