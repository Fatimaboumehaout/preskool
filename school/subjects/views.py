from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Subject

# --- LISTE DES MATIÈRES ---
@login_required(login_url='authentication:login')
def subject_list(request):
    subjects = Subject.objects.all()
    # Correction : Définition du dictionnaire context
    context = {
        'subjects': subjects
    }
    return render(request, 'subjects/subject_list.html', context)

# --- AJOUTER UNE MATIÈRE ---
@login_required(login_url='authentication:login')
def add_subject(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        description = request.POST.get('description')
        credits = request.POST.get('credits')

        # Validation simple pour éviter les erreurs de base de données
        if not name or not code:
            messages.error(request, 'Name and Code are required!')
            return render(request, 'subjects/add_subject.html')

        # Vérification des doublons
        if Subject.objects.filter(code=code).exists():
            messages.error(request, 'Subject with this code already exists!')
        elif Subject.objects.filter(name=name).exists():
            messages.error(request, 'Subject with this name already exists!')
        else:
            subject = Subject(
                name=name,
                code=code,
                description=description,
                credits=credits if credits else 1
            )
            subject.save()
            messages.success(request, 'Subject added successfully!')
            return redirect('subjects:subject_list')
    
    return render(request, 'subjects/add_subject.html')

# --- MODIFIER UNE MATIÈRE ---
@login_required(login_url='authentication:login')
def edit_subject(request, subject_id):
    # Récupère l'objet ou renvoie une erreur 404 si l'ID n'existe pas
    subject = get_object_or_404(Subject, id=subject_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        description = request.POST.get('description')
        credits = request.POST.get('credits')

        # Vérification des doublons (en excluant l'actuel)
        if Subject.objects.filter(code=code).exclude(id=subject_id).exists():
            messages.error(request, 'Subject with this code already exists!')
        elif Subject.objects.filter(name=name).exclude(id=subject_id).exists():
            messages.error(request, 'Subject with this name already exists!')
        else:
            subject.name = name
            subject.code = code
            subject.description = description
            subject.credits = credits if credits else 1
            subject.save()
            messages.success(request, 'Subject updated successfully!')
            return redirect('subjects:subject_list')
    
    return render(request, 'subjects/edit_subject.html', {'subject': subject})

# --- SUPPRIMER UNE MATIÈRE ---
@login_required(login_url='authentication:login')
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    
    # La suppression se fait généralement via POST pour la sécurité
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully!')
        return redirect('subjects:subject_list')
    
    return render(request, 'subjects/delete_subject.html', {'subject': subject})