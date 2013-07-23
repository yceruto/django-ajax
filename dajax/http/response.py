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
        """
        Constructor
        """
        serialized = json.dumps(data, sort_keys=settings.DEBUG)
        super(JsonHttpResponse, self).__init__(
            content=serialized,
            content_type='application/json'
        )

    def __len__(self):
        pass
