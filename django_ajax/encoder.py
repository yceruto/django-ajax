"""
Utils
"""
from __future__ import unicode_literals

import json
from datetime import date
from django.http.response import HttpResponseRedirectBase, HttpResponse
from django.template.response import TemplateResponse
from django.utils.encoding import force_str
from django.db.models.base import ModelBase
from decimal import Decimal


class LazyJSONEncoderMixin(object):
    """
    A JSONEncoder subclass that handle querysets and models objects.
    Add how handle your type of object here to use when dump json

    """

    def default(self, obj):
        # handles HttpResponse and exception content
        if issubclass(type(obj), HttpResponseRedirectBase):
            return obj['Location']
        elif issubclass(type(obj), TemplateResponse):
            return obj.rendered_content
        elif issubclass(type(obj), HttpResponse):
            return obj.content
        elif issubclass(type(obj), Exception) or isinstance(obj, bytes):
            return force_str(obj)

        # this handles querysets and other iterable types
        try:
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)

        # this handlers Models
        if isinstance(obj.__class__, ModelBase):
            return force_str(obj)

        if isinstance(obj, Decimal):
            return float(obj)

        if isinstance(obj, date):
            return obj.isoformat()

        return super(LazyJSONEncoderMixin, self).default(obj)


class LazyJSONEncoder(LazyJSONEncoderMixin, json.JSONEncoder):
    pass


def serialize_to_json(data, **kwargs):
    """
    A wrapper for simplejson.dumps with defaults as:

    cls=LazyJSONEncoder

    All arguments can be added via kwargs
    """
    kwargs['cls'] = kwargs.get('cls', LazyJSONEncoder)

    return json.dumps(data, **kwargs)
