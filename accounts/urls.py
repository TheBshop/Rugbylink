from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.SignUpView.as_view(), name='signup'),
    path('register/player/', views.PlayerSignUpView.as_view(), name='player_signup'),
    path('register/team/', views.TeamSignUpView.as_view(), name='team_signup'),
    path('register/agent/', views.AgentSignUpView.as_view(), name='agent_signup'),
    path('profile-setup/', views.profile_setup, name='profile_setup'),
]

