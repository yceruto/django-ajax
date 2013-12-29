+function ($) { "use strict";

    // AJAX CLASS DEFINITION
    // ======================

    var dismiss = '[data-ajax="true"]'
    var Ajax    = function (el) {
        $(el).on('click', dismiss, this.send)
    }

    Ajax.prototype.send = function (e) {
        var $this    = $(this)
        var method = $this.attr('data-method')
        var url = $this.attr('href') || $this.attr('action') || null
        var data = $this.attr('data-data') || null
        var onSuccess = $this.attr('data-success') || null

        if (!url) {
            alert('href or action attribute not found!')
            return
        }

        if (onSuccess) {
            eval('onSuccess = ' + onSuccess)
            if (!$.isFunction(onSuccess))
                onSuccess = null
        }

        method = method ? method.toLowerCase() : 'get'

        url = url && url.replace(/.*(?=#[^\s]*$)/, '') // strip for ie7

        data = data && data.replace(/'/g, '"') // Fix single quote

        if (e) e.preventDefault()

        try {
            data = $.parseJSON(data)
        } catch (e) {
            alert(method.toUpperCase() + ' ' + url + '   PARSE JSON ERROR' + '\n' + data + '\n' + e);
            return
        }

        if (ajax && $.isFunction(ajax))
            ajax(method, url, data, onSuccess)
        else
            alert('The ajax function not found. The jquery.ajax.js library is required.')
    }


    // ALERT PLUGIN DEFINITION
    // =======================

    var old = $.fn.ajax

    $.fn.ajax = function (option) {
        return this.each(function () {
            var $this = $(this)
            var data  = $this.data('abalt.ajax')

            if (!data) $this.data('abalt.ajax', (data = new Ajax(this)))
            if (typeof option == 'string') data[option].call($this)
        })
    }

    $.fn.ajax.Constructor = Ajax


    // ALERT NO CONFLICT
    // =================

    $.fn.ajax.noConflict = function () {
        $.fn.ajax = old
        return this
    }


    // ALERT DATA-API
    // ==============

    $(document).on('click.ajax.data-api', dismiss, Ajax.prototype.send)

}(jQuery);
