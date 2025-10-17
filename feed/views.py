from django.shortcuts import render
from django.views.generic import TemplateView

class FeedView(TemplateView):
    template_name = 'feed/home.html'

class PostDetailView(TemplateView):
    template_name = 'feed/post_detail.html'

class PostCreateView(TemplateView):
    template_name = 'feed/post_create.html'

def like_post(request, post_id):
    pass

def comment_post(request, post_id):
    pass