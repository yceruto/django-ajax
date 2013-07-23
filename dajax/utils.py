"""
Useful functions
"""
from django.http.response import HttpResponseRedirectBase, \
    HttpResponseNotAllowed, HttpResponse
from dajax.response import JsonHttpResponse


def response_to_dict(request, response):
    """
    Serialize the response to dictionary format
    """
    # not allowed response
    if isinstance(response, HttpResponseNotAllowed):
        return JsonHttpResponse({
            'success': False, 'status': response.status_code,
            'method': request.method, 'path': request.path,
            'allow': response['Allow']
        })

    # redirect response
    if issubclass(type(response), HttpResponseRedirectBase):
        return JsonHttpResponse({
            'success': False, 'status': response.status_code,
            'location': response['Location']
        })

    # simple response
    if issubclass(type(response), HttpResponse):
        return JsonHttpResponse({
            'success': True, 'status': response.status_code,
            'html': response.content
        })

    # exception
    if issubclass(type(response), Exception):
        return {
            'success': False, 'status': 500, 'exception': unicode(response),
            'path': request.path
        }

    # raw response
    return JsonHttpResponse({
        'success': True, 'status': 200, 'data': response
    })