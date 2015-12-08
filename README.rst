===========
django-ajax
===========

Fast and easy AJAX libraries for django projects.

.. image:: https://travis-ci.org/yceruto/django-ajax.png?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/yceruto/django-ajax
    
.. image:: https://img.shields.io/pypi/v/djangoajax.svg
    :alt: PYPI Package
    :target: https://pypi.python.org/pypi/djangoajax
    
.. image:: https://img.shields.io/pypi/dm/django-ajax.svg
    :alt: PYPI Download
    :target: https://pypi.python.org/pypi/djangoajax
    
.. image:: https://img.shields.io/pypi/pyversions/djangoajax.svg
    :alt: PYPI Versions
    :target: https://pypi.python.org/pypi/djangoajax
    
.. image:: https://img.shields.io/pypi/status/django-ajax.svg
    :alt: PYPI Status
    :target: https://pypi.python.org/pypi/djangoajax
    
.. image:: https://img.shields.io/pypi/l/djangoajax.svg
    :alt: PYPI License
    :target: https://pypi.python.org/pypi/djangoajax

Requirements
------------

* `python`_ >= 2.6
* `django`_ >= 1.5
* `jQuery`_ >= 1.5

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

3- Read usage section and enjoy its advantages!


Usage
-----

@ajax Decorator
~~~~~~~~~~~~~~~

.. code:: python

    from django_ajax.decorators import ajax

    @ajax
    def my_view(request)
        do_something()
        
When nothing is returned as result of view then returns (JSON format):

.. code:: javascript

    {"status": 200, "statusText": "OK", "content ": null}


**Sending custom data in the response**

.. code:: python

    @ajax
    def my_view(request):
        c = 2 + 3
        return {'result': c}
        
The result is send to the browser in the following way (JSON format)

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
        
The JSON response:

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

If you use AJAX quite frequently in your project, we suggest using the AJAXMiddleware described below.

Add ``django_ajax.middleware.AJAXMiddleware`` into the ``MIDDLEWARE_CLASSES`` list in ``settings.py``.

All your responses will be converted to JSON if the request was made by AJAX, otherwise is return a HttpResponse.

.. caution:: If you use this middleware cannot use ``@ajax`` decorator.


AJAXMixin for class-based views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``AJAXMixin`` is an object that calls the AJAX decorator.

.. code:: python

    from django.views.generic import TemplateView
    from django_ajax.mixin import AJAXMixin

    class SimpleView(AJAXMixin, TemplateView):
        template_name = 'home.html'

The JSON response:

.. code:: javascript

    {"status": 200, "statusText": "OK", "content": "<html>...</html>"}


AJAX on client side
~~~~~~~~~~~~~~~~~~~

Include ``jquery.ajax.min.js`` into ``base.html`` template:

.. code:: html

    <script type="text/javascript" src="{% static 'django_ajax/js/jquery.ajax.min.js' %}"></script>

Call to AJAX request using the ``ajaxPost`` or ``ajaxGet`` functions:

.. code:: html

    <script type="text/javascript">
        ajaxPost('/save', {'foo': 'bar'}, function(content){
            //onSuccess
            alert(content);
        })
    </script>

or

.. code:: html

    <script type="text/javascript">
        ajaxGet('/', function(content){
            //onSuccess
            alert(content);
        })
    </script>

If the response is not successful, it's shown an alert with the message appropriated.

**AJAX plugin** (Based on `eldarion-ajax <https://github.com/eldarion/eldarion-ajax>`_)

Include ``jquery.ajax-plugin.min.js`` into ``base.html`` template:

.. code:: html

    <script type="text/javascript" src="{% static 'django_ajax/js/jquery.ajax-plugin.min.js' %}"></script>

In this moment any tag with the attribute ``data-ajax`` will be controlled by ajax plugin. Each request is sent using AJAX and the response will be handle on JSON format.

The value of the attribute ``data-success`` will be used as callback function if the request is successful. This function is called with an argument that represent the content response:

.. code:: html

    <a href="/hello-world/" class="btn btn-primary" data-ajax="true" data-success="processResponse">Show Alert</a>

Where "processResponse" in this case is a callback function:

.. code:: html

   <script type="text/javascript">
        function processResponse(content) {
            do_something(content);
        }
    </script>

**Process fragments**

Inspired on `eldarion-ajax <https://github.com/eldarion/eldarion-ajax>`_ the data
received by the names ``'fragments'``, ``'inner-fragments'``, ``'append-fragments'``
or ``'prepend-fragments'`` will be processed by default, unless you pass in the
request the option "process-fragments" equal false. Here's an example:

.. code:: python

    @ajax
    def fragments_view(request):
        data = {
            'fragments': {
                '#id1': 'replace element with this content1'
            },
            'inner-fragments': {
                '#id2': 'replace inner content'
            },
            'append-fragments': {
                '.class1': 'append this content'
            },
            'prepend-fragments': {
                '.class2': 'prepend this content'
            }
        }
        return data

These data are sent in response:

.. code:: javascript

    {"status": 200, "statusText": "OK", "content": {
            "fragments": {"#id1": "replace element with this content1"},
            "inner-fragments": {"#id2": "replace inner content"},
            "append-fragments": {".class1": "append this content"},
            "prepend-fragments": {".class2": "prepend this content"}
        }}

Then, using AJAX (``ajax``, ``ajaxPost`` or ``ajaxGet``) functions these fragments to be processed automatically before calling to success function.

.. code:: html

   <script type="text/javascript">
        function fragments() {
            ajaxGet('/fragments-view-url', function(content){
                alert('The fragments was processed successfully!');
            });
        }
    </script>

If you do not want to process the fragments never, modify the AJAX configuration
that comes by default:

.. code:: html

    <script type="text/javascript">
        ajax.DEFAULTS["process-fragments"] = false; //true by default
    </script>

or as option on the request:

.. code:: html

    <script type="text/javascript">
        function fragments() {
            ajaxGet('/fragments-view-url', function(content){
                do_something_with(content.fragments);
            }, {"process-fragments": false});
        }
    </script>

Enjoy!
