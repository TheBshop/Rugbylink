from django.shortcuts import render
from django.views.generic import TemplateView

class ConnectionsListView(TemplateView):
    template_name = 'connections/list.html'

class FollowingListView(TemplateView):
    template_name = 'connections/following.html'

class FollowersListView(TemplateView):
    template_name = 'connections/followers.html'

def connect_user(request, user_id):
    pass

def disconnect_user(request, user_id):
    pass

class ConnectionRequestsView(TemplateView):
    template_name = 'connections/requests.html'

def accept_request(request, request_id):
    pass

def reject_request(request, request_id):
    pass