# home_auth/views.py 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages 
from .models import CustomUser
from .forms import CustomUserCreationForm, UserUpdateForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('authentication:dashboard')
        else:
            messages.error(request, 'Email ou mot de passe incorrect')
    
    return render(request, 'authentication/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès')
    return redirect('authentication:login')

@login_required
def dashboard_view(request):
    return render(request, 'Home/dashboard.html')

def signup_view(request): 
    if request.method == 'POST': 
        first_name = request.POST.get('first_name') 
        last_name = request.POST.get('last_name') 
        email = request.POST.get('email') 
        password = request.POST.get('password') 
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')  # student, teacher ou admin 

        # Validation simple
        if not all([first_name, last_name, email, password]):
            messages.error(request, 'Tous les champs sont obligatoires')
            return render(request, 'authentication/register.html')
        
        if password != confirm_password:
            messages.error(request, 'Les mots de passe ne correspondent pas')
            return render(request, 'authentication/register.html')

        try:
            # Créer l'utilisateur 
            user = CustomUser.objects.create_user( 
                username=email, 
                email=email, 
                first_name=first_name, 
                last_name=last_name, 
                password=password, 
            ) 

            # Assigner le rôle 
            if role == 'student': 
                user.is_student = True 
            elif role == 'teacher': 
                user.is_teacher = True 
            elif role == 'admin': 
                user.is_admin = True 
                user.is_staff = True  # Pour accéder à l'admin Django

            user.save() 
            login(request, user) 
            messages.success(request, 'Utilisateur créé avec succès!') 
            return redirect('authentication:dashboard') 
        except Exception as e:
            messages.error(request, f'Erreur lors de la création: {str(e)}')
            return render(request, 'authentication/register.html')
            
    return render(request, 'authentication/register.html')

# Vues pour la gestion des utilisateurs
class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        # Seuls les admins peuvent voir tous les utilisateurs
        if self.request.user.is_admin:
            return CustomUser.objects.all().order_by('-date_joined')
        else:
            # Les autres utilisateurs ne voient que leur propre profil
            return CustomUser.objects.filter(id=self.request.user.id)

class UserCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('authentication:user_list')

    def dispatch(self, request, *args, **kwargs):
        # Seuls les admins peuvent créer des utilisateurs
        if not request.user.is_admin:
            messages.error(request, "Vous n'avez pas la permission de créer des utilisateurs")
            return redirect('authentication:user_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Utilisateur créé avec succès!')
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('authentication:user_list')

    def dispatch(self, request, *args, **kwargs):
        # Les admins peuvent modifier n'importe qui, les autres seulement leur profil
        user = get_object_or_404(CustomUser, pk=kwargs['pk'])
        if not request.user.is_admin and request.user.id != user.id:
            messages.error(request, "Vous ne pouvez modifier que votre propre profil")
            return redirect('authentication:user_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Utilisateur mis à jour avec succès!')
        return super().form_valid(form)

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('authentication:user_list')

    def dispatch(self, request, *args, **kwargs):
        # Seuls les admins peuvent supprimer des utilisateurs
        if not request.user.is_admin:
            messages.error(request, "Vous n'avez pas la permission de supprimer des utilisateurs")
            return redirect('authentication:user_list')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Utilisateur supprimé avec succès!')
        return super().delete(request, *args, **kwargs)