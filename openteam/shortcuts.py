# -*- coding: utf-8 -*-

from django.shortcuts import redirect
from django.core.urlresolvers import reverse



def redirect_to_view(view_name, *args, **kwargs):
    return redirect(reverse(view_name, args=args, kwargs=kwargs))



