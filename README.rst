django-ajax-decorator
=====================

Powerful and easy AJAX decorator for django views

.. image:: https://travis-ci.org/yceruto/django-ajax-decorator.png?branch=master
    :target: https://travis-ci.org/yceruto/django-ajax-decorator

Installation
------------

Install django-ajax-decorator in your python environment

.. code:: sh

    $ pip install django-ajax-decorator


Usage
-----

Basic Example

.. code:: python

    from dajax.decorators import ajax

    @ajax()
    def my_view(request)
        do_something()
        
When nothing is returned as result of view then returns (JSON format):

.. code:: javascript

    {"success": true, "status": 200, "data": null}


Sending custom data in the response:

.. code:: python

    @ajax()
    def my_view(request):
        c = 2 + 3
        return {'result': c}
        
The result is send to the browser in the following way (JSON format)

.. code:: javascript

    {"success": true, "status": 200, "data": {"result": 5}}


Combining with other decorators:

.. code:: python

    @ajax()
    @login_required
    def my_view(request):
        # if the request.user is anonymous then this view not proceed 
        return {'user_id': request.user.id}
        
The result:

.. code:: javascript

    {"success": False, "status": 304, "location": "path to login"}
