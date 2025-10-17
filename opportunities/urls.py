from django.urls import path
from . import views

app_name = 'opportunities'

urlpatterns = [
    path('', views.OpportunityListView.as_view(), name='list'),
    path('<int:pk>/', views.OpportunityDetailView.as_view(), name='detail'),
    path('create/', views.OpportunityCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.OpportunityUpdateView.as_view(), name='edit'),
    path('my-opportunities/', views.MyOpportunitiesView.as_view(), name='my_opportunities'),
    path('my-applications/', views.MyApplicationsView.as_view(), name='my_applications'),
    path('<int:pk>/apply/', views.ApplicationCreateView.as_view(), name='apply'),
    path('application/<int:pk>/', views.ApplicationDetailView.as_view(), name='application_detail'),
]

