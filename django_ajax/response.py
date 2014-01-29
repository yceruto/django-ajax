# -*- coding: utf-8 -*-
"""
Responses
"""

from django.conf import settings
from django.http import HttpResponse
from django_ajax.utils import serialize_to_json


class JSONResponse(HttpResponse):
    """
    Return a JSON serialized HTTP response
    """

    def __init__(self, data):
        """
        This returns a object that we send as json content using
        utils.serialize_to_json, that is a wrapper to json.dumps
        method using a custom class to handle models and querysets. Put your
        options to serialize_to_json in kwargs, other options are used by
        response.
        """
        super(JSONResponse, self).__init__(
            content=serialize_to_json(data, sort_keys=settings.DEBUG),
            content_type='application/json'
        )