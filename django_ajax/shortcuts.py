# -*- coding: utf-8 -*-
"""
Shortcuts
"""

from django.http.response import HttpResponseRedirectBase, \
    Http404, REASON_PHRASES, HttpResponse
from django.template.response import TemplateResponse
from django.utils.encoding import force_unicode
from django_ajax.response import JSONResponse


def render_to_json(response):
    """
    Determine the appropriate content and create the JSON response
    """
    # determine the status code
    if hasattr(response, 'status_code'):
        status_code = response.status_code
    elif issubclass(type(response), Http404):
        status_code = 404
    elif issubclass(type(response), Exception):
        status_code = 500
    else:
        status_code = 200

    data = {}

    # TODO: add optional process for fragments
    if isinstance(response, dict):
        for key in ['fragments', 'inner-fragments', 'append-fragments',
                    'prepend-fragments']:
            if key in response:
                data.update({
                    key: response.pop(key)
                })

    data.update({
        'status': status_code,
        'statusText': REASON_PHRASES.get(status_code, 'UNKNOWN STATUS CODE'),
        'content': response
    })

    return JSONResponse(data)

