/* ========================================================================
 * Django Ajax v2.2.10
 * https://github.com/yceruto/django-ajax/
 * Copyright 2014 Abalt
 * ======================================================================== */

 ;(function ($) { "use strict";

    // AJAX CLASS DEFINITION
    // ======================
	var dismiss_submit = '[data-ajax-submit]';
    var dismiss = '[data-ajax]',
        Ajax = function (el) {
            $(el).on('click', dismiss, this.send);
            $(el).on('submit', dismiss_submit, this.submit);
        };

    Ajax.prototype.send = function (e) {
        var $this = $(this),
            method = $this.data('method'),
            url = $this.attr('href') || $this.data('href') || $this.data('url') || null,
            data = $this.data('data') || null,
            onError = $this.data('error') || null;

        if (e) e.preventDefault();

        if (!url) {
            alert('href, data-href or data-url attribute not found!');
            return
        }

        if (onError) {
            try {
                onError = window[onError];
                if (!$.isFunction(onError))
                    onError = null
            } catch (e) {
                alert(e.name + '\n' + e.message);
            }
        }

        method = method ? method.toLowerCase() : 'get';

        url = url && url.replace(/.*(?=#[^\s]*$)/, ''); // strip for ie7

        data = data && data.replace(/'/g, '"'); // Fix single quote

        try {
            data = $.parseJSON(data);
        } catch (e) {
            alert(e.name + '\n' + e.message);
            return
        }

        if (ajax && $.isFunction(ajax))
            ajax(url, {
                method: method,
                data: data,
                onSuccess: function(response) {
                    processData(response, $this);
                },
                onError: onError
            });
        else
            alert('jquery.ajax.js is required');
    };

	Ajax.prototype.submit = function(e) {
        var $form = $(this),
            url = $form.attr('action'),
            method = $form.attr('method'),
            data = $form.serialize(),
            redirect_inner_selector = $form.data('redirect-inner'),
            options = redirect_inner_selector ? {
                onRedirect: function (url) {
                    ajaxGet(url, function(content){
                        $(redirect_inner_selector).html(content);
                    })
                }
            } : {};

        e.preventDefault();

        method = method ? method.toLowerCase() : 'get';

        ajaxMethod(method, url, data, function(content){
            var response = {};
            response.content = content;
            processData(response, $form);
        }, options);
	};

    function find_father_child(father, child, $el) {
        var closest_father_child = undefined;

        if (father && child) {
            closest_father_child = $el.closest(father).find(child);
            if (closest_father_child.length == 0) {
                closest_father_child = undefined;
            }
        }

        return closest_father_child;
    }

    function processData(response, $el) {
        var success_function = $el.data('success'),
            replace_selector = $el.data('replace'),
            replace_closest_selector = $el.data('replace-closest'),
            replace_inner_selector = $el.data('replace-inner'),
            replace_closest_inner_selector = $el.data('replace-closest-inner'),
            replace_closest_father_child = find_father_child($el.data('replace-father'), $el.data('replace-child'), $el),
            replace_closest_father_child_inner = find_father_child($el.data('replace-father'), $el.data('replace-child-inner'), $el),
            append_selector = $el.data('append'),
            prepend_selector = $el.data('prepend'),
            refresh_selector = $el.data('refresh'),
            refresh_closest_selector = $el.data('refresh-closest'),
            refresh_inner_selector = $el.data('refresh-inner'),
            refresh_closest_father_child = find_father_child($el.data('refresh-father'), $el.data('refresh-child'), $el),
            refresh_closest_father_child_inner = find_father_child($el.data('refresh-father'), $el.data('refresh-child-inner'), $el),
            clear_selector = $el.data('clear'),
            clear_closest_selector = $el.data('clear-closest'),
            remove_selector = $el.data('remove'),
            remove_closest_selector = $el.data('remove-closest');

        if (replace_selector) {
            $(replace_selector).replaceWith(response.content)
        }

        if (replace_closest_selector) {
            $el.closest(replace_closest_selector).replaceWith(response.content)
        }

        if (replace_inner_selector) {
            $(replace_inner_selector).html(response.content)
        }

        if (replace_closest_father_child) {
            replace_closest_father_child.replaceWith(response.content)
        }

        if (replace_closest_father_child_inner) {
            replace_closest_father_child_inner.html(response.content)
        }

        if (replace_closest_inner_selector) {
            $el.closest(replace_closest_inner_selector).html(response.content)
        }

        if (append_selector) {
            $(append_selector).append(response.content)
        }

        if (prepend_selector) {
            $(prepend_selector).prepend(response.content)
        }

        if (refresh_selector) {
            $.each($(refresh_selector), function(index, value) {
                ajaxGet($(value).data('refresh-url'), function(content) {
                    $(value).replaceWith(content)
                })
            })
        }

        if (refresh_inner_selector) {
            $.each($(refresh_inner_selector), function(index, value) {
                ajaxGet($(value).data('refresh-url'), function(content) {
                    $(value).html(content)
                })
            })
        }

        if (refresh_closest_selector) {
            $.each($(refresh_closest_selector), function(index, value) {
                ajaxGet($(value).data('refresh-url'), function(content) {
                    $el.closest($(value)).replaceWith(content)
                })
            })
        }

        if (refresh_closest_father_child) {
            $.each(refresh_closest_father_child, function(index, value) {
                ajaxGet($(value).data('refresh-url'), function(content) {
                    $(value).replaceWith(content)
                })
            })
        }

        if (refresh_closest_father_child_inner) {
            $.each(refresh_closest_father_child_inner, function(index, value) {
                ajaxGet($(value).data('refresh-url'), function(content) {
                    $(value).html(content)
                })
            })
        }

        if (clear_selector) {
            $(clear_selector).html('')
        }

        if (remove_selector) {
            $(remove_selector).remove()
        }

        if (clear_closest_selector) {
            $el.closest(clear_closest_selector).html('')
        }

        if (remove_closest_selector) {
            $el.closest(remove_closest_selector).remove()
        }

        if (success_function) {
            try {
                success_function = window[success_function];
                $.isFunction(success_function) && success_function(response.content);
            } catch (e) {
                alert(e.name + '\n' + e.message);
            }
        }
    }


    // AJAX PLUGIN DEFINITION
    // =======================

    var old = $.fn.ajax;

    $.fn.ajax = function (option) {
        return this.each(function () {
            var $this = $(this),
                data  = $this.data('django.ajax');

            if (!data) $this.data('django.ajax', (data = new Ajax(this)));
            if (typeof option == 'string') data[option].call($this)
        })
    };

    $.fn.ajax.Constructor = Ajax;


    // AJAX NO CONFLICT
    // =================

    $.fn.ajax.noConflict = function () {
        $.fn.ajax = old;
        return this
    };


    // AJAX DATA-API
    // ==============

    $(document).on('click.ajax.data-api', dismiss, Ajax.prototype.send);
    $(document).on('submit.ajax.data-api', dismiss_submit, Ajax.prototype.submit)
})(jQuery);
