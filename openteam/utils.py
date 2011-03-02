# -*- mode: python -*- coding: utf-8 -*-
import logging
import sys
import re
import urllib
from datetime import datetime
from decimal import Decimal
from lxml import etree

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.template import loader

from types import ListType, DictType

# --------------------------------------------------------------------------- #
SINGLE_LINE = re.compile('.+')

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
    url = "http://www.typograf.ru/webservice/"
    params = urllib.urlencode( {'text': text.encode('utf-8'),'chr':'UTF-8'} )
    f = urllib.urlopen(url, params)
    return f.read()



def get_logger():
    logger = logging.getLogger()
    hdlr = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)-8s"%(message)s"','%Y-%m-%d %a %H:%M:%S')

    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)

    return logger


def debug(msg):
    logger = get_logger()
    logger.setLevel(logging.DEBUG)
    logger.debug(msg)


def html2text(text):
    return etree.tostring(
        etree.HTML(text),
        encoding='utf8', method='text'
    )



def send_email(to, tpl, context):
    """
    """
    to = "<%s>" % to
    # here we check that email subject isn't multiline
    dirty_subject = loader.render_to_string('email/%s.subj.html' % tpl, context)
    clean_subject = SINGLE_LINE.match(dirty_subject).group()

    message = EmailMessage(
        subject = clean_subject,
        body    = loader.render_to_string('email/%s.body.html' % tpl, context),
        from_email = settings.DEFAULT_FROM_EMAIL,
        to = [to, ],
    )
    message.content_subtype = 'plain'

    try:
        message.send()

    except Exception, e:
        debug(e)

