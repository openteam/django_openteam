from django.template import Library, TemplateSyntaxError
from django.conf import settings
import urllib, bitly

register = Library()

@register.inclusion_tag('openteam/tinyurl.html', takes_context=True)
def bitly_url(context):
    api = bitly.Api(login=settings.BITLY_LOGIN, apikey=settings.BITLY_APIKEY)
    url_original = 'http://' + context['request'].META['HTTP_HOST'] + context['request'].META['PATH_INFO']
    try:
        url_shorten = api.shorten(url_original)
    except TypeError:
        url_shorten = "#"
    context.update({
        'url': url_shorten
    })
    return context

