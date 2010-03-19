from django.conf import settings


def static(request):
    """Adds static media context variables to the context"""
    return {
        'CSS_URL': settings.CSS_URL,
        'IMG_URL': settings.IMG_URL,
        'JS_URL': settings.JS_URL,
    }

