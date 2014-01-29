# -*- coding: utf-8 -*-
"""
Utils
"""

from django.utils.encoding import force_unicode
from django.db.models.base import ModelBase

import json


class LazyJSONEncoder(json.JSONEncoder):
    """
    A JSONEncoder subclass that handle querysets and models objects.
    Add how handle your type of object here to use when when dump json
    """

    def default(self, o):
        # this handles querysets and other iterable types
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)

        # this handlers Models
        if issubclass(o, ModelBase):
            return force_unicode(o)

        return super(LazyJSONEncoder, self).default(o)


def serialize_to_json(obj, *args, **kwargs):
    """
    A wrapper for simplejson.dumps with defaults as:

    cls=LazyJSONEncoder

    All arguments can be added via kwargs
    """

    kwargs['cls'] = kwargs.get('cls', LazyJSONEncoder)

    return json.dumps(obj, *args, **kwargs)
