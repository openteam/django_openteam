# -*- mode: python -*- coding: utf-8 -*-
from datetime import datetime
from decimal import Decimal
from django.conf import settings
from django.db import models
import logging
import sys
from types import ListType, DictType

# --------------------------------------------------------------------------- #

def json_encode(data):
    """
    The main issues with django's default json serializer is that properties
    that had been added to a object dynamically are being ignored (and it also
    has problems with some models).
    """

    def _any(data):
        ret = None

        if type(data) is ListType:
            ret = _list(data)

        elif type(data) is DictType:
            ret = _dict(data)

        elif isinstance(data, Decimal):
            # json.dumps() cant handle Decimal
            ret = unicode(data)

        elif isinstance(data, models.query.QuerySet):
            # Actually its the same as a list ...
            ret = _list(data)

        elif isinstance(data, models.Model):
            ret = _model(data)

        elif isinstance(data, models.FileField):
            ret = unicode(data.url) if data.url else None

        elif isinstance(data, datetime):
            ret = unicode(data)

        else:
            ret = data

        return ret

    def _model(data):
        ret = {}

        # If we only have a model, we only want to encode the fields.
        for f in data._meta.fields:
            ret[f.attname] = _any(getattr(data, f.attname))

            # And additionally encode arbitrary properties that had been added.
            fields = dir(data.__class__) + ret.keys()
            add_ons = [k for k in dir(data) if k not in fields]

            for k in add_ons:
                ret[k] = _any(getattr(data, k))
        return ret

    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))
        return ret

    def _dict(data):
        ret = {}
        for k,v in data.items():
            ret[k] = _any(v)
        return ret

    ret = _any(data)
    return ret



def typograf(text):
    """Das russisch typograph. Achtung dreckschwein.
    """
    import urllib
    url = "http://www.typograf.ru/webservice/"
    params = urllib.urlencode( {'text': text.encode('utf-8'),'chr':'UTF-8'} )
    f = urllib.urlopen(url, params)
    return f.read()



def get_logger():
    logger = logging.getLogger()
    hdlr = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('[%(asctime)s]%(levelname)-8s"%(message)s"','%Y-%m-%d %a %H:%M:%S')

    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)

    return logger


def debug(msg):
    logger = get_logger()
    logger.setLevel(logging.DEBUG)
    logger.debug(msg)

