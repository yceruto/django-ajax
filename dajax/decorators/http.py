from functools import wraps
from django.http import HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotAllowed
from django.http.response import HttpResponseRedirectBase
from django.utils.decorators import available_attrs
from dajax.http.response import JsonHttpResponse


def ajax(mandatory=True):
    """
    Decorator who guesses the user response type and translates to a serialized
    JSON response. Usage::

        @ajax()
        def my_view(request):
            do_something()
            # will send {'success': True, 'data': null, 'status': 200}

        @ajax()
        def my_view(request):
            return {'key': 'value'}
            # will send {'success': True, 'data': {'key': 'value'}, 'status': 200}

        @ajax()
        def my_view(request):
            return HttpResponse('<h1>Hi! AJAX MANDATORY</h1>')
            # will send {'success': True, 'html': '<h1>Hi! AJAX MANDATORY</h1>', 'status': 200}

        @ajax()
        def my_view(request):
            return redirect('home')
            # will send {'success': False, 'location': '/', 'status': 304}

        # combination with others decorators:

        @ajax()
        @login_required
        @require_POST
        def my_view(request):
            pass
            # if request user is not authenticated then the @login_required
            # decorator redirect to login page.
            # will send {'success': False, 'location': '/login', 'status': 304}

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

            if mandatory or request.is_ajax():
                try:
                    # run view
                    data = func(request, *args, **kwargs)

                    # response not allowed
                    if isinstance(data, HttpResponseNotAllowed):
                        return JsonHttpResponse({
                            'success': False, 'status': data.status_code,
                            'method': request.method, 'path': request.path,
                            'allow': data['Allow']
                        })

                    # response redirect
                    if issubclass(type(data), HttpResponseRedirectBase):
                        return JsonHttpResponse({
                            'success': False, 'status': data.status_code,
                            'location': data['Location']
                        })

                    # simple response
                    if issubclass(type(data), HttpResponse):
                        return JsonHttpResponse({
                            'success': True, 'status': data.status_code,
                            'html': data.content
                        })

                    # raw data
                    return JsonHttpResponse({
                        'success': True, 'status': 200, 'data': data
                    })

                except Exception as exception:
                    return JsonHttpResponse({
                        'success': False, 'status': 500,
                        'exception': exception.message, 'path': request.path,
                        'view': func.func_name
                    })
            else:
                # conventional response
                return func(request, *args, **kwargs)

        return inner

    return decorator