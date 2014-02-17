django-ajax
=====================

Powerful and easy AJAX libraries for django projects.

.. image:: https://travis-ci.org/yceruto/django-ajax.png?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/yceruto/django-ajax
    
.. image:: https://badge.fury.io/py/abalt-django-ajax.png
    :alt: PYPI Package
    :target: https://pypi.python.org/pypi/abalt-django-ajax    

Requirements
------------

* python>=2.6
* django>=1.3


Installation
------------

Install django-ajax in your python environment

1- Download and install package:

.. code:: sh

    $ pip install abalt-django-ajax

or simply with:

.. code:: sh

    $ python setup.py install

2- Add ``'django_ajax'`` into the ``INSTALLED_APPS`` list.

3- Read usage section and enjoy its advantages!


AJAX Decorator Usage
--------------------

Basic Example

.. code:: python

    from django_ajax.decorators import ajax

    @ajax
    def my_view(request)
        do_something()
        
When nothing is returned as result of view then returns (JSON format):

.. code:: javascript

    {"status": 200, "statusText": "OK", "content ": null}


Sending custom data in the response:

.. code:: python

    @ajax
    def my_view(request):
        c = 2 + 3
        return {'result': c}
        
The result is send to the browser in the following way (JSON format)

.. code:: javascript

    {"status": 200, "statusText": "OK", "content": {"result": 5}}


Combining with others decorators:

.. code:: python

    @ajax
    @login_required
    def my_view(request):
        # if the request.user is anonymous then this view not proceed 
        return {'user_id': request.user.id}
        
The JSON response:

.. code:: javascript

    {"status": 302, "statusText": "FOUND", "content": "/login"}


Template response:

.. code:: python

    @ajax
    def my_view(request):
        return render(request, 'home.html')

The JSON response:

.. code:: javascript

    {"status": 200, "statusText": "OK", "content": "<html>...</html>"}


Catch exceptions:

.. code:: python

    @ajax
    def my_view(request):
        a = 23 / 0  # this line throws an exception
        return a

The JSON response:

.. code:: javascript

    {"status": 500, "statusText": "INTERNAL SERVER ERROR", "content": "integer division or modulo by zero"}


AJAX Middleware Usage
---------------------

.. code:: python

Add ``django_ajax.middleware.AJAXMiddleware`` into the ``MIDDLEWARE_CLASSES`` list.

All your responses will be converted to JSON if the request was made by AJAX, otherwise is return a HttpResponse.

Note: If you use this middleware should not use the AJAX decorator.


AJAX Mixin for class-based views
--------------------------------

.. code:: python

    from django_ajax.mixin import AJAXMixin

    class SimpleView(AJAXMixin, TemplateView):
        template_name = 'home.html'

The JSON response:

.. code:: javascript

    {"status": 200, "statusText": "OK", "content": "<html><title>Home</title>...</html>"}


AJAX Client
-----------

Use the jquery.ajax.min.js as static file into base template

.. code:: html

    <script type="text/javascript" src="{% static 'django_ajax/js/jquery.ajax.min.js' %}"></script>

Call to Ajax request using the "ajaxPost" or "ajaxGet" functions.

.. code:: html

    <script type="text/javascript">
        ajaxGet('/', {}, function(content){
            //onSuccess
            alert(content);
        })
    </script>

If the response is not successful, it´s shown an alert with the message appropriated.

AJAX plugin
-----------

Include the jquery.ajax-plugin.min.js as static file into base template

.. code:: html

    <script type="text/javascript" src="{% static 'django_ajax/js/jquery.ajax-plugin.min.js' %}"></script>

In this moment any tag with the attribute "data-ajax" will be handle by ajax plugin. Each request is sent
using the XMLHttpRequest object (AJAX) and the response is returned on JSON format.

The success data will be used as callback function if the request is successful. The callback function is
called with a param that represent the response content:

.. code:: html

    <a href="/hello-world/" class="btn btn-primary" data-ajax="true" data-success="success">Show Alert</a>

Where "success" is a function:

.. code:: html

   <script type="text/javascript">
        function success(content) {
            alert(content);
        }
    </script>

Process fragments based on https://github.com/eldarion/eldarion-ajax

Enjoy!
