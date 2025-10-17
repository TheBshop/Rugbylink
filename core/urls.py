from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('set-language/', views.set_language, name='set_language'),
    path('debug-lang/', views.debug_language, name='debug_language'),
]
