from django.template import Library, TemplateSyntaxError
from django.conf import settings

register = Library()

@register.inclusion_tag('openteam/helpers/submit.html')
def submit_tag(value):
    return { 'value': value }

