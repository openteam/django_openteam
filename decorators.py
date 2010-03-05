from django.core import exceptions
from django.http import HttpResponse
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
            return HttpResponse('This view is requires AJAX request', status=400)
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
            return HttpResponse('This view is requires POST method', status=400)
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

def render_to(template):
    """
    Decorator for Django views that sends returned dict to render_to_response function
    with given template and RequestContext as context instance.

    If view doesn't return dict then decorator simply returns output.
    Additionally view can return two-tuple, which must contain dict as first
    element and string with template name as second. This string will
    override template name, given as parameter

    Parameters:

     - template: template name to use
    """
    def renderer(func):
        @wraps(func)
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(template, output, RequestContext(request))
            return output
        return wrapper
    return renderer

