
abalt-django-ajax
=====================

Powerful and easy AJAX toolkit for django applications. Contains ajax decorator, ajax middleware, shortcuts and more.

.. image:: https://travis-ci.org/yceruto/abalt-django-ajax.png?branch=master
    :target: https://travis-ci.org/yceruto/abalt-django-ajax

Requirements
------------

* python>=2.6
* django>=1.3


Installation
------------

Install abalt-django-ajax in your python environment

1- Download and install package:

.. code:: sh

    $ python abalt-django-ajax install

2- Add ``'abalt_ajax'`` into the ``INSTALLED_APPS`` list.

3- Read usage section and enjoy their advantage!


AJAX Decorator Usage
--------------------

Basic Example

.. code:: python

    from abalt_ajax.decorators import ajax

    @ajax
    def my_view(request)
        do_something()
        
When nothing is returned as result of view then returns (JSON format):

.. code:: javascript

    {"success": true, "status": 200, "data": null}


Sending custom data in the response:

.. code:: python

    @ajax
    def my_view(request):
        c = 2 + 3
        return {'result': c}
        
The result is send to the browser in the following way (JSON format)

.. code:: javascript

    {"success": true, "status": 200, "data": {"result": 5}}


Combining with others decorators:

.. code:: python

    @ajax
    @login_required
    def my_view(request):
        # if the request.user is anonymous then this view not proceed 
        return {'user_id': request.user.id}
        
The JSON response:

.. code:: javascript

    {"success": False, "status": 302, "location": "/login"}


Template response:

.. code:: python

    @ajax
    def my_view(request):
        return render(request, 'home.html')

The JSON response:

.. code:: javascript

    {"success": True, "status": 200, "data": "<html>...</html>"}


Catch exceptions:

.. code:: python

    @ajax
    def my_view(request):
        a = 23 / 0  # this line throws an exception
        return a

The JSON response:

.. code:: javascript

    {"success": False, "status": 500, "exception": "integer division or modulo by zero"}


AJAX Middleware Usage
---------------------

.. code:: python

Add ``abalt_ajax.middleware.AjaxMiddleware`` into the ``MIDDLEWARE_CLASSES`` list.

Then, all your responses will be converted to JSON if the request was made by AJAX, otherwise is return an HttpResponse.

Note: If you use this middleware should not use the AJAX decorator.


AJAX response with class-based views
------------------------------------

.. code:: python

    class SimpleView(AJAXResponseMixin, TemplateView):
        template_name = 'home.html'

The JSON response:

.. code:: javascript

    {"success": True, "status": 200, "data": "<html><title>Home</title>...</html>"}


Client side
-----------

Use the abalt_ajax.js as static file into base template

.. code:: html

    <script type="text/javascript" src="{% static 'js/abalt_ajax.js' %}"></script>

Later, use the "post" or "get" functions for call ajax and fire the callback function if successful.

.. code:: html

    <script type="text/javascript">
        get('/home', null, function(result){
            alert(result.data);
        })
    </script>

If the response is not successful, is show an alert with the message appropriated.

Enjoy!