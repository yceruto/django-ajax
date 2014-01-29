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
        super(JSONResponse, self).__init__(
            content=serialize_to_json(data, sort_keys=settings.DEBUG),
            content_type='application/json'
        )