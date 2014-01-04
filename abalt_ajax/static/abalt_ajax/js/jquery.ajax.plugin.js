/* ========================================================================
 * Abalt Django Ajax: jquery.ajax.plugin.js v1.0
 * https://github.com/yceruto/abalt-django-ajax/
 * Copyright 2014 Yonel Ceruto Glez
 * ======================================================================== */

 ;(function ($) { "use strict";

    // AJAX CLASS DEFINITION
    // ======================

    var dismiss = '[data-ajax="true"]',
        Ajax = function (el) {
            $(el).on('click', dismiss, this.send)
        };

    Ajax.prototype.send = function (e) {
        var $this = $(this),
            method = $this.attr('data-method'),
            url = $this.attr('href') || $this.attr('action') || null,
            data = $this.attr('data-data') || null,
            onSuccess = $this.attr('data-success') || null,
            onError = $this.attr('data-error') || null;

        if (!url) {
            alert('href or action attribute not found!');
            return
        }

        if (onSuccess) {
            eval('onSuccess = ' + onSuccess);
            if (!$.isFunction(onSuccess))
                onSuccess = null
        }

        if (onError) {
            eval('onError = ' + onError);
            if (!$.isFunction(onError))
                onError = null
        }

        method = method ? method.toLowerCase() : 'get';

        url = url && url.replace(/.*(?=#[^\s]*$)/, ''); // strip for ie7

        data = data && data.replace(/'/g, '"'); // Fix single quote

        if (e) e.preventDefault();

        try {
            data = $.parseJSON(data)
        } catch (e) {
            alert(method.toUpperCase() + ' ' + url + '   PARSE JSON ERROR' + '\n' + data + '\n' + e);
            return
        }

        if (ajax && $.isFunction(ajax))
            ajax(method, url, data, onSuccess, onError);
        else
            alert('jquery.ajax.js is required')
    };


    // ALERT PLUGIN DEFINITION
    // =======================

    var old = $.fn.ajax;

    $.fn.ajax = function (option) {
        return this.each(function () {
            var $this = $(this),
                data  = $this.data('abalt.ajax');

            if (!data) $this.data('abalt.ajax', (data = new Ajax(this)));
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
