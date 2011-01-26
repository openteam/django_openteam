from django.core import exceptions
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from functools import wraps

# --------------------------------------------------------------------------- #

def ajax_only(view):
    """
    Performs the view if it requested with XMLHttpRequest or output
    error message otherwise

    """
    def wrap(request, *args, **kwargs):
        if request.is_ajax():
            return view(request, *args, **kwargs)
        else:
            return HttpResponse('This view accepts only AJAX request object', status=400)
    return wrap

# --------------------------------------------------------------------------- #

def post_only(view):
    """
    Performs the view if it requested with POST or output
    error message otherwise

    """
    def wrap(request, *args, **kwargs):
        if request.method == 'POST':
            return view(request, *args, **kwargs)
        else:
            return HttpResponse('This view accepts only POST method', status=400)
    return wrap


def staff_required(view):
    """
    Checks whether user is authenticated and has stuff permissions

    """
    def guard(request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_staff:
            return view(request,  *args, **kwargs)
        raise exceptions.PermissionDenied()

    return guard

# --------------------------------------------------------------------------- #

