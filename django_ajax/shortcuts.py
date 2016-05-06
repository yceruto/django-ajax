"""
Shortcuts
"""
from __future__ import unicode_literals

import logging

from django.conf import settings
from django.http.response import Http404, HttpResponseServerError
from django.views.debug import ExceptionReporter

from django_ajax.response import JSONResponse

logger = logging.getLogger(__name__)

# Available since django 1.6
REASON_PHRASES = {
    100: 'CONTINUE',
    101: 'SWITCHING PROTOCOLS',
    102: 'PROCESSING',
    200: 'OK',
    201: 'CREATED',
    202: 'ACCEPTED',
    203: 'NON-AUTHORITATIVE INFORMATION',
    204: 'NO CONTENT',
    205: 'RESET CONTENT',
    206: 'PARTIAL CONTENT',
    207: 'MULTI-STATUS',
    208: 'ALREADY REPORTED',
    226: 'IM USED',
    300: 'MULTIPLE CHOICES',
    301: 'MOVED PERMANENTLY',
    302: 'FOUND',
    303: 'SEE OTHER',
    304: 'NOT MODIFIED',
    305: 'USE PROXY',
    306: 'RESERVED',
    307: 'TEMPORARY REDIRECT',
    400: 'BAD REQUEST',
    401: 'UNAUTHORIZED',
    402: 'PAYMENT REQUIRED',
    403: 'FORBIDDEN',
    404: 'NOT FOUND',
    405: 'METHOD NOT ALLOWED',
    406: 'NOT ACCEPTABLE',
    407: 'PROXY AUTHENTICATION REQUIRED',
    408: 'REQUEST TIMEOUT',
    409: 'CONFLICT',
    410: 'GONE',
    411: 'LENGTH REQUIRED',
    412: 'PRECONDITION FAILED',
    413: 'REQUEST ENTITY TOO LARGE',
    414: 'REQUEST-URI TOO LONG',
    415: 'UNSUPPORTED MEDIA TYPE',
    416: 'REQUESTED RANGE NOT SATISFIABLE',
    417: 'EXPECTATION FAILED',
    418: "I'M A TEAPOT",
    422: 'UNPROCESSABLE ENTITY',
    423: 'LOCKED',
    424: 'FAILED DEPENDENCY',
    426: 'UPGRADE REQUIRED',
    428: 'PRECONDITION REQUIRED',
    429: 'TOO MANY REQUESTS',
    431: 'REQUEST HEADER FIELDS TOO LARGE',
    500: 'INTERNAL SERVER ERROR',
    501: 'NOT IMPLEMENTED',
    502: 'BAD GATEWAY',
    503: 'SERVICE UNAVAILABLE',
    504: 'GATEWAY TIMEOUT',
    505: 'HTTP VERSION NOT SUPPORTED',
    506: 'VARIANT ALSO NEGOTIATES',
    507: 'INSUFFICIENT STORAGE',
    508: 'LOOP DETECTED',
    510: 'NOT EXTENDED',
    511: 'NETWORK AUTHENTICATION REQUIRED',
}


def render_to_json(response, *args, **kwargs):
    """
    Creates the main structure and returns the JSON response.
    """
    # determine the status code
    if hasattr(response, 'status_code'):
        status_code = response.status_code
    elif issubclass(type(response), Http404):
        status_code = 404
    elif issubclass(type(response), Exception):
        status_code = 500
        logger.exception(str(response), extra={'request': kwargs.pop('request', None)})
        
        if settings.DEBUG:
            import sys
            reporter = ExceptionReporter(None, *sys.exc_info())
            text = reporter.get_traceback_text()
            response = HttpResponseServerError(text, content_type='text/plain')
        else:
            response = HttpResponseServerError("An error occured while processing an AJAX request.", content_type='text/plain')
    else:
        status_code = 200

    # creating main structure
    data = {
        'status': status_code,
        'statusText': REASON_PHRASES.get(status_code, 'UNKNOWN STATUS CODE'),
        'content': response
    }

    return JSONResponse(data,  *args, **kwargs)

