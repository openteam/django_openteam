from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.template import Library, TemplateSyntaxError
from django.utils.translation import ugettext_lazy as _

from django_openteam.utils import debug


register = Library()

try:
    from django_openid_auth.forms import OpenIDLoginForm

    @register.inclusion_tag('forms/openid.html', takes_context=True)
    def openid_form(context):
        """Tag for rendering openid sign in form and return it in place"""
        context.update({
            'form': OpenIDLoginForm()
        })

        return context

except ImportError, ex:
    debug(_("Failed to import django_openid_auth: %(message)s") % {
        'message': ex,
        })


@register.inclusion_tag('forms/auth.html', takes_context=True)
def auth_form(context):
    """Tag for rendering authentication form and return it in place"""
    context.update({
        'form': AuthenticationForm()
    })
    return context




@register.inclusion_tag('forms/reset_pass.html', takes_context=True)
def password_reset_form(context):
    """Tag for rendering reset_pass form and return it in place"""

    context.update({
        'form': PasswordResetForm()
    })

    return context

