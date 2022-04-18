from __future__ import absolute_import
from app import views
import django

try:
    try:
        from django.conf.urls import patterns, include, url
    except ImportError:
        from django.conf.urls import include, url
except ImportError:
    from django.urls import include, re_path

if django.VERSION < (1, 8):
    urlpatterns = patterns('',
        url(r'^ajax/foo$', views.foo_view, name='foo'),
        url(r'^ajax/login-required$', views.login_required_view, name='login_required'),
        url(r'^ajax/render$', views.render_view, name='render'),
        url(r'^ajax/render-class-based-view$', views.SimpleView.as_view(), name='render_class_based_view'),
        url(r'^ajax/exception$', views.exception_view, name='exception'),
        url(r'^ajax/raise-exception$', views.raise_exception_view, name='raise_exception'),
    )
elif django.VERSION < (4, 0):
    urlpatterns = [
        url(r'^ajax/foo$', views.foo_view, name='foo'),
        url(r'^ajax/login-required$', views.login_required_view, name='login_required'),
        url(r'^ajax/render$', views.render_view, name='render'),
        url(r'^ajax/render-class-based-view$', views.SimpleView.as_view(), name='render_class_based_view'),
        url(r'^ajax/exception$', views.exception_view, name='exception'),
        url(r'^ajax/raise-exception$', views.raise_exception_view, name='raise_exception'),
    ]
else:
    urlpatterns = [
        re_path(r'^ajax/foo$', views.foo_view, name='foo'),
        re_path(r'^ajax/login-required$', views.login_required_view, name='login_required'),
        re_path(r'^ajax/render$', views.render_view, name='render'),
        re_path(r'^ajax/render-class-based-view$', views.SimpleView.as_view(), name='render_class_based_view'),
        re_path(r'^ajax/exception$', views.exception_view, name='exception'),
        re_path(r'^ajax/raise-exception$', views.raise_exception_view, name='raise_exception'),
    ]
