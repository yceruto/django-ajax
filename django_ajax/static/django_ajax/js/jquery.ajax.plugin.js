/* ========================================================================
 * Django Ajax: jquery.ajax.plugin.js v1.0
 * https://github.com/yceruto/django-ajax/
 * Copyright 2014 Yonel Ceruto Glez
 * ======================================================================== */

 ;(function ($) { "use strict";

    // AJAX CLASS DEFINITION
    // ======================

    var dismiss = '[data-ajax]',
        Ajax = function (el) {
            $(el).on('click', dismiss, this.send)
        };

    Ajax.prototype.send = function (e) {
        var $this = $(this),
            method = $this.data('method'),
            url = $this.attr('href') || $this.data('href') || $this.data('url') || null,
            data = $this.data('data') || null,
            onSuccess = $this.data('success') || null,
            onError = $this.data('error') || null;

        if (e) e.preventDefault();

        if (!url) {
            alert('href, data-href or data-url attribute not found!');
            return
        }

        if (onSuccess) {
            try {
                onSuccess = window[onSuccess];
                if (!$.isFunction(onSuccess))
                    onSuccess = null
            } catch (e) {
                alert(e);
            }
        }

        if (onError) {
            try {
                onError = window[onError];
                if (!$.isFunction(onError))
                    onError = null
            } catch (e) {
                alert(e);
            }
        }

        method = method ? method.toLowerCase() : 'get';

        url = url && url.replace(/.*(?=#[^\s]*$)/, ''); // strip for ie7

        data = data && data.replace(/'/g, '"'); // Fix single quote

        try {
            data = $.parseJSON(data)
        } catch (e) {
            alert(method.toUpperCase() + ' ' + url + '   PARSE JSON ERROR' + '\n' + data + '\n' + e);
            return
        }

        if (ajax && $.isFunction(ajax))
            ajax(url, {
                method: method,
                data: data,
                onSuccess: function(response) {
                    $.isFunction(onSuccess) && onSuccess(response.content);
                    processData(response, $this);
                },
                onError: onError
            });
        else
            alert('jquery.ajax.js is required')
    };

    function processData(response, $el) {
        var replace_selector = $el.data('replace'),
            replace_closest_selector = $el.data('replace-closest'),
            replace_inner_selector = $el.data('replace-inner'),
            replace_closest_inner_selector = $el.data('replace-closest-inner'),
            append_selector = $el.data('append'),
            prepend_selector = $el.data('prepend'),
            refresh_selector = $el.data('refresh'),
            refresh_closest_selector = $el.data('refresh-closest'),
            clear_selector = $el.data('clear'),
            remove_selector = $el.data('remove'),
            clear_closest_selector = $el.data('clear-closest'),
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

        if (refresh_closest_selector) {
            $.each($(refresh_closest_selector), function(index, value) {
                ajaxGet($(value).data('refresh-url'), function(content) {
                    $el.closest($(value)).replaceWith(content)
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

        //process fragments
        if (response.fragments) {
            for (var s in response.fragments) {
                $(s).replaceWith(response.fragments[s])
            }
        }

        if (response['inner-fragments']) {
            for (var i in response['inner-fragments']) {
                $(i).html(response['inner-fragments'][i])
            }
        }

        if (response['append-fragments']) {
            for (var a in response['append-fragments']) {
                $(a).append(response['append-fragments'][a])
            }
        }

        if (response['prepend-fragments']) {
            for (var p in response['prepend-fragments']) {
                $(p).prepend(response['prepend-fragments'][p])
            }
        }
    }


    // ALERT PLUGIN DEFINITION
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


    // ALERT NO CONFLICT
    // =================

    $.fn.ajax.noConflict = function () {
        $.fn.ajax = old;
        return this
    };


    // ALERT DATA-API
    // ==============

    $(document).on('click.ajax.data-api', dismiss, Ajax.prototype.send)

})(jQuery);
