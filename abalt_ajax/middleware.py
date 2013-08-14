"""
Django middlewares
"""
from abalt_ajax.shortcuts import render_to_json


class AjaxMiddleware(object):
    """
    Ajax Middleware Class
    """
    def process_response(self, request, response):
        if request.is_ajax():
            return render_to_json(request, response)
        return response

    def process_exception(self, request, exception):
        if request.is_ajax():
            return exception
