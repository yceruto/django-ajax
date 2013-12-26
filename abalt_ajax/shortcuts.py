"""
Ajax Shortcuts
"""
from django.http import HttpResponse
from django.http.response import HttpResponseRedirectBase, \
    HttpResponseNotAllowed, Http404, REASON_PHRASES, HttpResponseForbidden, \
    HttpResponseNotFound, HttpResponseServerError, HttpResponseGone, \
    HttpResponseBadRequest, HttpResponseNotModified
from django.template.response import TemplateResponse
from abalt_ajax.response import JsonHttpResponse


def render_to_json(request, response):
    """
    Render response to JSON
    """
    data = {
        'status': response.status_code if hasattr(response, 'status_code') else 0,
        'status_text': response.reason_phrase if hasattr(response, 'reason_phrase') else 'UNKNOWN STATUS CODE',
        'path': request.path
    }

    if isinstance(response, HttpResponseNotAllowed):
        data.update({
            'method': request.method
        })
    elif issubclass(type(response), HttpResponseRedirectBase):
        data.update({
            'location': response['Location']
        })
    elif issubclass(type(response), HttpResponseForbidden) or \
            issubclass(type(response), HttpResponseBadRequest) or \
            issubclass(type(response), HttpResponseNotFound) or \
            issubclass(type(response), HttpResponseGone) or \
            issubclass(type(response), HttpResponseNotModified) or \
            issubclass(type(response), HttpResponseServerError):
        pass
    elif issubclass(type(response), TemplateResponse):
        data.update({
            'data': response.rendered_content
        })
    elif issubclass(type(response), HttpResponse):
        data.update({
            'data': response.content
        })
    elif issubclass(type(response), Http404):
        data.update({
            'status': 404, 'status_text': REASON_PHRASES[404]
        })
    elif issubclass(type(response), Exception):
        data.update({
            'status': 500, 'status_text': REASON_PHRASES[500],
            'exception': unicode(response),
        })
    else:
        data.update({
            'data': response.content if hasattr(response, 'content') else response
        })

    return JsonHttpResponse(data)

