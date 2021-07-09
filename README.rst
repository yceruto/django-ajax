===========
django-ajax
===========

Fast and easy AJAX libraries for django applications.

.. image:: https://api.travis-ci.com/yceruto/django-ajax.svg?branch=master
    :alt: Master Build Status
    :target: https://travis-ci.com/github/yceruto/django-ajax
    
.. image:: https://img.shields.io/pypi/v/djangoajax.svg
    :alt: PYPI Package
    :target: https://pypi.python.org/pypi/djangoajax
    
.. image:: https://img.shields.io/pypi/status/django-ajax.svg
    :alt: PYPI Status
    :target: https://pypi.python.org/pypi/djangoajax
    
.. image:: https://img.shields.io/pypi/l/djangoajax.svg
    :alt: PYPI License
    :target: https://pypi.python.org/pypi/djangoajax

Requirements
------------

``3.x``

* `python`_ >=3.5
* `django`_ >=2.0

``2.x``

* `python`_ >=2.7
* `django`_ >=1.7,<2.0

.. _`python`: http://www.python.org/
.. _`django`: https://djangoproject.com
.. _`jQuery`: http://jquery.com

Installation
------------

Install django-ajax in your python environment

1- Download and install package:

.. code:: sh

    $ pip install djangoajax

Through Github:

.. code:: sh

    pip install -e git://github.com/yceruto/django-ajax#egg=djangoajax

or simply with:

.. code:: sh

    $ python setup.py install

2- Add ``'django_ajax'`` into the ``INSTALLED_APPS`` list.

3- Read usage section and enjoy this feature!


Usage
-----

@ajax Decorator
~~~~~~~~~~~~~~~

.. code:: python

    from django_ajax.decorators import ajax

    @ajax
    def my_view(request):
        do_something()
        
When the view does not return anything, you will receive this response (JSON format):

.. code:: javascript

    {"status": 200, "statusText": "OK", "content ": null}


**Sending content**

.. code:: python

    @ajax
    def my_view(request):
        c = 2 + 3
        return {'result': c}
        
The whole result is converted into a JSON format as part of the `content` element:

.. code:: javascript

    {"status": 200, "statusText": "OK", "content": {"result": 5}}


**Combining with others decorators**

.. code:: python

    from django.contrib.auth.decorators import login_required
    from django_ajax.decorators import ajax

    @ajax
    @login_required
    def my_view(request):
        # if the request.user is anonymous then this view not proceed 
        return {'user_id': request.user.id}
        
The location or path of the redirection response will be given in the `content` item, 
also the `status` and `statusText` will reflect what is going on:

.. code:: javascript

    {"status": 302, "statusText": "FOUND", "content": "/login"}


**Template response**

.. code:: python

    from django.shortcuts import render
    from django_ajax.decorators import ajax

    @ajax
    def my_view(request):
        return render(request, 'home.html')

The JSON response:

.. code:: javascript

    {"status": 200, "statusText": "OK", "content": "<html>...</html>"}


**Catch exceptions**

.. code:: python

    @ajax
    def my_view(request):
        a = 23 / 0  # this line throws an exception
        return a

The JSON response:

.. code:: javascript

    {"status": 500, "statusText": "INTERNAL SERVER ERROR", "content": "integer division or modulo by zero"}


AJAXMiddleware
~~~~~~~~~~~~~~

If you are using AJAX at all times in your project, we suggest you activate the AJAXMiddleware described below.

Add ``django_ajax.middleware.AJAXMiddleware`` to the ``MIDDLEWARE_CLASSES`` list in ``settings.py`` and all your responses will be converted to JSON whereas the request was made via AJAX, otherwise it will return a normal HttpResponse.

.. caution:: If this middleware is activated you cannot use the ``@ajax`` decorator. That will cause double JSON conversion.


AJAXMixin for class-based views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``AJAXMixin`` is an object that call to AJAX decorator.

.. code:: python

    from django.views.generic import TemplateView
    from django_ajax.mixin import AJAXMixin

    class SimpleView(AJAXMixin, TemplateView):
        template_name = 'home.html'

The JSON response:

.. code:: javascript

    {"status": 200, "statusText": "OK", "content": "<html>...</html>"}

Enjoy And Share!
