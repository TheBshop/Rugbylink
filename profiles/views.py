from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .models import PlayerProfile, TeamProfile, AgentProfile
from .forms import PlayerProfileForm, TeamProfileForm, AgentProfileForm

User = get_user_model()


class PlayerProfileDetailView(DetailView):
    model = PlayerProfile
    template_name = 'profiles/player_detail.html'
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object.user
        return context


class PlayerProfileCreateView(LoginRequiredMixin, CreateView):
    model = PlayerProfile
    form_class = PlayerProfileForm
    template_name = 'profiles/player_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Player profile created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profiles:player_detail', kwargs={'pk': self.object.pk})


class PlayerProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = PlayerProfile
    form_class = PlayerProfileForm
    template_name = 'profiles/player_form.html'

    def get_queryset(self):
        return PlayerProfile.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Player profile updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profiles:player_detail', kwargs={'pk': self.object.pk})


class TeamProfileDetailView(DetailView):
    model = TeamProfile
    template_name = 'profiles/team_detail.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object.user
        return context


class TeamProfileCreateView(LoginRequiredMixin, CreateView):
    model = TeamProfile
    form_class = TeamProfileForm
    template_name = 'profiles/team_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Team profile created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profiles:team_detail', kwargs={'pk': self.object.pk})


class TeamProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = TeamProfile
    form_class = TeamProfileForm
    template_name = 'profiles/team_form.html'

    def get_queryset(self):
        return TeamProfile.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Team profile updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profiles:team_detail', kwargs={'pk': self.object.pk})


class AgentProfileDetailView(DetailView):
    model = AgentProfile
    template_name = 'profiles/agent_detail.html'
    context_object_name = 'agent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object.user
        return context


class AgentProfileCreateView(LoginRequiredMixin, CreateView):
    model = AgentProfile
    form_class = AgentProfileForm
    template_name = 'profiles/agent_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Agent profile created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profiles:agent_detail', kwargs={'pk': self.object.pk})


class AgentProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = AgentProfile
    form_class = AgentProfileForm
    template_name = 'profiles/agent_form.html'

    def get_queryset(self):
        return AgentProfile.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Agent profile updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profiles:agent_detail', kwargs={'pk': self.object.pk})