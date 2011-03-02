# -*- coding: utf-8 -*-

from django.db.models import Manager
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from utils import json_encode

import json


json_enc = json.dumps
json_dec = json.loads



def get_object_or_none(klass, *args, **kwargs):
    if isinstance(klass, Manager):
        manager = klass
        klass = manager.model
    else:
        manager = klass._default_manager

        try:
            return manager.get(*args, **kwargs)
        except klass.DoesNotExist:
            return None


def redirect_to_view(view_name, *args, **kwargs):
    return redirect(reverse(view_name, args=args, kwargs=kwargs))


def json_response(data, mimetype='application/json'):
    class JsonResponse(HttpResponse):
        def __init__(self, data, mimetype=mimetype):
            HttpResponse.__init__(self,
                content  = json_enc(json_encode(data)),
                mimetype = mimetype,
            )
    return JsonResponse(data)

