# -*- coding: utf-8 -*-
import json
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from .utils import json_encode

def redirect_to_view(view_name, *args, **kwargs):
    return redirect(reverse(view_name, args=args, kwargs=kwargs))


def render_to_json(data, mimetype='application/json'):

    class JSONResponse(HttpResponse):
    
        def __init__(self, data, mimetype):
            super(JSONResponse, self).__init__(
                content=json.dumps(json_encode(data)),
                mimetype=mimetype)

    return JSONResponse(data, mimetype)
