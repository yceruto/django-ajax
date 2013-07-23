"""
Http responses
"""
import json
from django.conf import settings
from django.http import HttpResponse


class JsonHttpResponse(HttpResponse):
    """
    Return a JSON serialized HTTP response
    """
    def __init__(self, data):
        super(JsonHttpResponse, self).__init__(
            content=json.dumps(data, sort_keys=settings.DEBUG),
            content_type='application/json'
        )