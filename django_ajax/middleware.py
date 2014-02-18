"""
Middleware
"""
from __future__ import unicode_literals

from django_ajax.shortcuts import render_to_json


class AJAXMiddleware(object):
    """
    AJAX Middleware that decides when to convert the response to JSON.
    """

    def process_response(self, request, response):
        """
        If the request was made by AJAX then convert response to JSON,
        otherwise return the original response.
        """
        if request.is_ajax():
            return render_to_json(response)
        return response

    def process_exception(self, request, exception):
        """
        Catch exception if the request was made by AJAX,
        after will become up on JSON.
        """
        if request.is_ajax():
            return exception
