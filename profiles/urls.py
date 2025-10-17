from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    # Player URLs
    path('player/<int:pk>/', views.PlayerProfileDetailView.as_view(), name='player_detail'),
    path('player/create/', views.PlayerProfileCreateView.as_view(), name='player_create'),
    path('player/<int:pk>/edit/', views.PlayerProfileUpdateView.as_view(), name='player_edit'),
    
    # Team URLs
    path('team/<int:pk>/', views.TeamProfileDetailView.as_view(), name='team_detail'),
    path('team/create/', views.TeamProfileCreateView.as_view(), name='team_create'),
    path('team/<int:pk>/edit/', views.TeamProfileUpdateView.as_view(), name='team_edit'),
    
    # Agent URLs
    path('agent/<int:pk>/', views.AgentProfileDetailView.as_view(), name='agent_detail'),
    path('agent/create/', views.AgentProfileCreateView.as_view(), name='agent_create'),
    path('agent/<int:pk>/edit/', views.AgentProfileUpdateView.as_view(), name='agent_edit'),
]

