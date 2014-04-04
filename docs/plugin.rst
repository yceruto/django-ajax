This is an example to how use ajax plugin 

The available options are:
    - replace
    - replace-closest
    - replace-inner
    - replace-father used with replace-child or replace-child-inner
    - append
    - prepend
    - refresh            
    - refresh-closest
    - refresh-inner
    - refresh-father used with refresh-child or refresh-child-inner
    - clear
    - clear-closest
    - remove-closest
    - data-success obligatory when use links

First, include in your template 

.. code:: html

    <script type="text/javascript" src="{% static 'django_ajax/js/jquery.ajax.min.js' %}"></script>
    <script type="text/javascript" src="{% static 'django_ajax/js/jquery.ajax-plugin.min.js' %}"></script>

If you want to use a link should include data-ajax="" as atribute and the options that you want.

.. code:: html

    <a href="/hello-world/" class="btn btn-primary" data-ajax="" data-success="processResponse">Show Alert</a>

For include a URL reference use href, data-href or data-url, it is util for example in refresh option.
e.g

.. code:: html

    <div data-url="/list/" id="myList"></div>
    <a href="/hello-world/" class="btn btn-primary" refresh-inner="#myList" data-ajax="" data-success="function(){}">Display List</a>

If you want to use a form should include data-ajax-submit="" as atribute and the options that you want.
e.g

.. code:: html

    <div id="father">
        <div id="myList"></div>
        <div id="editList">
            <form action="/edit/" method="post" data-ajax-submit="" replace-father="father"
                  replace-child-inner="#myList" onsubmit="return false;">
              ...
            </form>
        </div>
        <button data-href="/create/" replace-inner="editList" data-ajax="" data-success="function(){}" > create </button>
    </div>

.. note:

    Put action and method attributes is important. 
    Rewrite onsubmit attribute to prevent redirections.
