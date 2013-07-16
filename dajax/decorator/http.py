from functools import wraps
from django.http import HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotAllowed
from django.http.response import HttpResponseRedirectBase
from django.utils.decorators import available_attrs
from dajax.http.response import JsonHttpResponse


def render_to_json(mandatory=True):
    """
    Decorator to serialize the HTTP response to JSON. Usage::

        @render_to_json()
        def my_view(request):
            # return a dictionary on a compulsory basis
            return {'key': 'value', ...}
        or

        @render_to_json(False)
        def my_view(request):
            # use request.ajax() to see if the request was made by AJAX
            if request.is_ajax():
                return {'key': 'value'}

            return HttpResponse('Hi! Traditional Response')

    Note that when 'mandatory' is true and return a subclass of HttpResponse,
    does not send to the browser a JSON response
    """
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            data = func(request, *args, **kwargs)

            if (mandatory or request.is_ajax()) and \
                    not issubclass(type(data), HttpResponse):
                return JsonHttpResponse(data)

            return data

        return inner

    return decorator


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
            return HttpResponse('Hi! AJAX MANDATORY')
            # will send {'success': True, 'html': 'Hi! AJAX MANDATORY', 'status': 200}

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
        @render_to_json(mandatory)
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
                        return dict(success=False, status=data.status_code,
                                    method=request.method, path=request.path,
                                    allow=data['Allow'])

                    # response redirect
                    if issubclass(type(data), HttpResponseRedirectBase):
                        return dict(success=False, status=data.status_code,
                                    location=data['Location'])

                    # simple response
                    if issubclass(type(data), HttpResponse):
                        return dict(success=True, status=data.status_code,
                                    html=data.content)

                    return dict(success=True, status=200, data=data)

                except Exception as exception:
                    return dict(success=False, status=500,
                                exception=exception.message, path=request.path,
                                view=func.func_name)
            else:
                # traditional response
                return func(request, *args, **kwargs)

        return inner

    return decorator