# -*- coding: utf-8 -*-
"""
Middleware
"""

from django_ajax.shortcuts import render_to_json


class AJAXMiddleware(object):
    """
    AJAX Middleware Class
    """
    def process_response(self, request, response):
        if request.is_ajax():
            return render_to_json(response)
        return response

    def process_exception(self, request, exception):
        if request.is_ajax():
            return exception
