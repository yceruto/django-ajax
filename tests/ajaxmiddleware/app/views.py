from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import Http404

# We're using `django_ajax.middleware.AJAXMiddleware` in settings
# so we don't need to use `@ajax` and `AJAXMixin` decorators


def foo_view(request):
    return {'foo': True}


@login_required
def login_required_view(request):
    # if the request.user is anonymous then this view not proceed
    return {'user_id': request.user.id}


def render_view(request):
    return render(request, 'hello.html')


class SimpleView(TemplateView):
    template_name = 'hello.html'


def exception_view(request):
    a = 23 / 0  # this line throws an exception
    return a
    

def raise_exception_view(request):
    raise Http404
