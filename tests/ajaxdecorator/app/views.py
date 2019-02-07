from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import Http404

from django_ajax.decorators import ajax
from django_ajax.mixin import AJAXMixin


@ajax
def foo_view(request):
    return {'foo': True}


@ajax
@login_required
def login_required_view(request):
    # if the request.user is anonymous then this view not proceed
    return {'user_id': request.user.id}


@ajax
def render_view(request):
    return render(request, 'hello.html')


class SimpleView(AJAXMixin, TemplateView):
    template_name = 'hello.html'


@ajax
def exception_view(request):
    a = 23 / 0  # this line throws an exception
    return a
    

@ajax
def raise_exception_view(request):
    raise Http404
