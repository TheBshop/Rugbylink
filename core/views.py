from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import translation
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

User = get_user_model()


def home(request):
    """Home page view"""
    context = {}
    
    if request.user.is_authenticated:
        # Get unread messages count for authenticated users
        unread_messages_count = 0  # We'll implement this when messaging is ready
        context['unread_messages_count'] = unread_messages_count
    
    return render(request, 'core/home.html', context)


def search(request):
    """Search functionality across users"""
    query = request.GET.get('q', '').strip()
    results = []
    
    if query:
        # Search across all user types
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        ).select_related('player_profile', 'team_profile', 'agent_profile')[:20]
        
        results = users
    
    context = {
        'query': query,
        'results': results,
    }
    
    if request.user.is_authenticated:
        context['unread_messages_count'] = 0  # We'll implement this when messaging is ready
    
    return render(request, 'core/search.html', context)


def set_language(request):
    """Set user language preference"""
    if request.method == 'POST':
        language = request.POST.get('language')
        if language and language in [lang[0] for lang in settings.LANGUAGES]:
            # Set language in session
            request.session['django_language'] = language
            
            # Set language cookie
            response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language, max_age=settings.LANGUAGE_COOKIE_AGE)
            return response
    
    return redirect('core:home')


def debug_language(request):
    """Debug language settings"""
    from django.utils import translation
    from django.conf import settings
    
    context = {
        'current_language': translation.get_language(),
        'available_languages': settings.LANGUAGES,
        'session_language': request.session.get(translation.LANGUAGE_SESSION_KEY),
        'cookie_language': request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME),
        'request_language': request.LANGUAGE_CODE if hasattr(request, 'LANGUAGE_CODE') else 'Not set',
        'browser_language': request.META.get('HTTP_ACCEPT_LANGUAGE', 'Not detected'),
    }
    
    return render(request, 'core/debug_language.html', context)