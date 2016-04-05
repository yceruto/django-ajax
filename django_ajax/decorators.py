"""
Decorators
"""
from __future__ import unicode_literals

from functools import wraps

from django.http import HttpResponseBadRequest
from django.utils.decorators import available_attrs

from django_ajax.shortcuts import render_to_json


def ajax(function=None, mandatory=True, **ajax_kwargs):
    """
    Decorator who guesses the user response type and translates to a serialized
    JSON response. Usage::

        @ajax
        def my_view(request):
            do_something()
            # will send {'status': 200, 'statusText': 'OK', 'content': null}

        @ajax
        def my_view(request):
            return {'key': 'value'}
            # will send {'status': 200, 'statusText': 'OK',
                         'content': {'key': 'value'}}

        @ajax
        def my_view(request):
            return HttpResponse('<h1>Hi!</h1>')
            # will send {'status': 200, 'statusText': 'OK',
                         'content': '<h1>Hi!</h1>'}

        @ajax
        def my_view(request):
            return redirect('home')
            # will send {'status': 302, 'statusText': 'FOUND', 'content': '/'}

        # combination with others decorators:

        @ajax
        @login_required
        @require_POST
        def my_view(request):
            pass
            # if request user is not authenticated then the @login_required
            # decorator redirect to login page.
            # will send {'status': 302, 'statusText': 'FOUND',
                         'content': '/login'}

            # if request method is 'GET' then the @require_POST decorator return
            # a HttpResponseNotAllowed response.
            # will send {'status': 405, 'statusText': 'METHOD NOT ALLOWED',
                         'content': null}

    """
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            if mandatory and not request.is_ajax():
                return HttpResponseBadRequest()

            if request.is_ajax():
                # return json response
                try:
                    return render_to_json(func(request, *args, **kwargs), **ajax_kwargs)
                except Exception as exception:
                    return render_to_json(exception, request=request)
            else:
                # return standard response
                return func(request, *args, **kwargs)

        return inner

    if function:
        return decorator(function)

    return decorator
