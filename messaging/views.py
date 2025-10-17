from django.shortcuts import render
from django.views.generic import TemplateView

class InboxView(TemplateView):
    template_name = 'messaging/inbox.html'

class ConversationView(TemplateView):
    template_name = 'messaging/conversation.html'

def start_conversation(request, user_id):
    pass

def send_message(request, conversation_id):
    pass