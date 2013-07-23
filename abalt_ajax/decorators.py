"""
Django decorators
"""
from functools import wraps
from django.http import HttpResponseBadRequest
from django.utils.decorators import available_attrs
from abalt_ajax.shortcuts import render_to_json


def ajax(function=None, mandatory=True):
    """
    Decorator who guesses the user response type and translates to a serialized
    JSON response. Usage::

        @ajax
        def my_view(request):
            do_something()
            # will send {'success': True, 'data': null, 'status': 200}

        @ajax
        def my_view(request):
            return {'key': 'value'}
            # will send {'success': True, 'data': {'key': 'value'}, +
                         'status': 200}

        @ajax
        def my_view(request):
            return HttpResponse('<h1>Hi! AJAX MANDATORY</h1>')
            # will send {'success': True, 'html': '<h1>Hi! AJAX MANDATORY</h1>',
                         'status': 200}

        @ajax
        def my_view(request):
            return redirect('home')
            # will send {'success': False, 'location': '/', 'status': 302}

        # combination with others decorators:

        @ajax
        @login_required
        @require_POST
        def my_view(request):
            pass
            # if request user is not authenticated then the @login_required
            # decorator redirect to login page.
            # will send {'success': False, 'location': '/login', 'status': 302}

            # if request method is 'GET' then the @require_POST decorator return
            # a HttpResponseNotAllowed response.
            # will send {'success': False, 'status': 405, 'method': 'GET',
                         'path': 'url from my_view', 'allow': 'POST'}

    """
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            if mandatory and not request.is_ajax():
                return HttpResponseBadRequest()

            if request.is_ajax():
                try:
                    # json response
                    return render_to_json(
                        request, func(request, *args, **kwargs))
                except Exception as exception:
                    return render_to_json(request, exception)
            else:
                # conventional response
                return func(request, *args, **kwargs)

        return inner

    if function:
        return decorator(function)
    return decorator
