"""
Django middlewares
"""
from dajax.http import JsonHttpResponse
from dajax.utils import response_to_dict


class AjaxMiddleware(object):
    """
    Ajax Middleware Class
    """
    def process_response(self, request, response):
        if request.is_ajax():
            return JsonHttpResponse(response_to_dict(request, response))
        return response

    def process_exception(self, request, exception):
        if request.is_ajax():
            return exception
