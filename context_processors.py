from django.conf import settings
from django.contrib.sites.models import Site

from datetime import datetime

def static(request):
    """Adds static media context variables to the context"""
    return {
        'SITE': Site.objects.get_current(),
        'CSS_URL': settings.CSS_URL,
        'IMG_URL': settings.IMG_URL,
        'JS_URL': settings.JS_URL,
    }

