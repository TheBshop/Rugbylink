from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, PlayerRegistrationForm, TeamRegistrationForm, AgentRegistrationForm
from .models import CustomUser


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('feed:home')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('core:home')


class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response


class PlayerSignUpView(CreateView):
    model = CustomUser
    form_class = PlayerRegistrationForm
    template_name = 'accounts/player_signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Player account created successfully! Please log in.')
        return response


class TeamSignUpView(CreateView):
    model = CustomUser
    form_class = TeamRegistrationForm
    template_name = 'accounts/team_signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Team account created successfully! Please log in.')
        return response


class AgentSignUpView(CreateView):
    model = CustomUser
    form_class = AgentRegistrationForm
    template_name = 'accounts/agent_signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Agent account created successfully! Please log in.')
        return response


@login_required
def profile_setup(request):
    """Redirect users to appropriate profile setup based on user type"""
    user = request.user
    
    if user.user_type == 'PLAYER':
        return redirect('profiles:player_create')
    elif user.user_type == 'TEAM':
        return redirect('profiles:team_create')
    elif user.user_type == 'AGENT':
        return redirect('profiles:agent_create')
    
    return redirect('feed:home')