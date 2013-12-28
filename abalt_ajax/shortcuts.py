"""
Ajax Shortcuts
"""
from django.http.response import HttpResponseRedirectBase, \
    Http404, REASON_PHRASES, HttpResponse
from django.template.response import TemplateResponse
from abalt_ajax.response import JsonHttpResponse


def render_to_json(response):
    """
    Render response to JSON
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

    # define the response text
    if issubclass(type(response), HttpResponseRedirectBase):
        response_text = response['Location']
    elif issubclass(type(response), TemplateResponse):
        response_text = response.rendered_content
    elif issubclass(type(response), HttpResponse):
        response_text = response.content
    elif issubclass(type(response), Exception):
        response_text = unicode(response)
    else:
        response_text = response

    data = {
        'status': status_code,
        'statusText': REASON_PHRASES.get(status_code, 'UNKNOWN STATUS CODE'),
        'responseText': response_text
    }

    return JsonHttpResponse(data)

