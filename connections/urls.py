from django.urls import path
from . import views

app_name = 'connections'

urlpatterns = [
    path('', views.ConnectionsListView.as_view(), name='list'),
    path('following/', views.FollowingListView.as_view(), name='following'),
    path('followers/', views.FollowersListView.as_view(), name='followers'),
    path('connect/<int:user_id>/', views.connect_user, name='connect'),
    path('disconnect/<int:user_id>/', views.disconnect_user, name='disconnect'),
    path('requests/', views.ConnectionRequestsView.as_view(), name='requests'),
    path('request/accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('request/reject/<int:request_id>/', views.reject_request, name='reject_request'),
]

