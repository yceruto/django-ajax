"""
Shortcuts
"""
from django.http import HttpResponse
from django.http.response import HttpResponseRedirectBase, \
    HttpResponseNotAllowed
from abalt_ajax.response import JsonHttpResponse


def render_to_json(request, response):
    """
    Render response to JSON
    """
    if isinstance(response, HttpResponseNotAllowed):
        data = {
            'success': False, 'status': response.status_code,
            'method': request.method, 'path': request.path,
            'allow': response['Allow']
        }
    elif issubclass(type(response), HttpResponseRedirectBase):
        data = {
            'success': False, 'status': response.status_code,
            'location': response['Location']
        }
    elif issubclass(type(response), Exception):
        data = {
            'success': False, 'status': 500, 'exception': unicode(response),
            'path': request.path
        }
    elif issubclass(type(response), HttpResponse):
        data = {
            'success': True, 'status': response.status_code,
            'data': response.content
        }
    else:
        data = {
            'success': True, 'status': 200, 'data': response
        }

    return JsonHttpResponse(data)

