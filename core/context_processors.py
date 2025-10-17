from django.conf import settings


def language_context(request):
    """Add language information to template context"""
    # Get language from session, cookie, or default
    language = request.session.get('django_language') or request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, 'en')
    
    return {
        'LANGUAGE_CODE': language,
        'LANGUAGES': settings.LANGUAGES,
        'current_language': language,
    }
