"""
Ajax Shortcuts
"""
from django.http.response import HttpResponseRedirectBase, \
    Http404, REASON_PHRASES, HttpResponse
from django.template.response import TemplateResponse
from abalt_ajax.response import JsonHttpResponse


def render_to_json(response):
    """
    Guess response
    """
    # define the status code
    if hasattr(response, 'status_code'):
        status_code = response.status_code
    elif issubclass(type(response), Http404):
        status_code = 404
    elif issubclass(type(response), Exception):
        status_code = 500
    else:
        status_code = 200

    # define the content of the response
    if issubclass(type(response), HttpResponseRedirectBase):
        content = response['Location']
    elif issubclass(type(response), TemplateResponse):
        content = response.rendered_content
    elif issubclass(type(response), HttpResponse):
        content = response.content
    elif issubclass(type(response), Exception):
        content = unicode(response)
    else:
        content = response

    data = {
        'status': status_code,
        'statusText': REASON_PHRASES.get(status_code, 'UNKNOWN STATUS CODE'),
        'content': content
    }

    return JsonHttpResponse(data)

