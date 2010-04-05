from django.conf import settings
from django.contrib.sites.models import Site


def static(request):
    """Adds static media context variables to the context"""
    return {
        'site': Site.objects.get(pk = settings.SITE_ID),
        'CSS_URL': settings.CSS_URL,
        'IMG_URL': settings.IMG_URL,
        'JS_URL': settings.JS_URL,
    }

