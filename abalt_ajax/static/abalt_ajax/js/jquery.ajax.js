function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

+function ($) { "use strict";

    // AJAX SETUP
    // ======================

    $.ajaxSetup({
        crossDomain: false // obviates need for sameOrigin test
    });


    // AJAX CLASS DEFINITION
    // ======================

    var dismiss = '[data-ajax="true"]'
    var Ajax    = function (el) {
        $(el).on('click', dismiss, this.ajax)
    }

    Ajax.prototype.ajax = function (e) {
        var $this    = $(this)
        var method = $this.attr('data-method')
        var url = $this.attr('href') || $this.attr('action') || null
        var data = $this.attr('data-data') || null

        if (!url) {
            alert('href or action attribute not found!')
            return
        }

        method = method ? method.toLowerCase() : 'get'

        url = url && url.replace(/.*(?=#[^\s]*$)/, '') // strip for ie7

        // Fix the single quote
        data = data && data.replace(/'/g, '"')

        if (e) e.preventDefault()

        try {
            data = $.parseJSON(data)
        } catch (e) {
            alert(method.toUpperCase() + ' ' + url + '   PARSE JSON ERROR' + '\n' + data + '\n' + e);
            return
        }

        $.ajax({
            url: url,
            type: method,
            data: data,
            beforeSend: function ( xhr, settings ) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }

                //TODO: custom beforeSend function
            },
            success: function( response ){
                if (response.status == 200) {
                    //TODO: fire onsuccess
                    alert(response.responseText)
                } else {
                    //TODO: custom fail function
                    alert(method.toUpperCase() + ' ' + url + '   ' + response.status + ' ' + response.statusText + '\n' + response.responseText)

                    switch (response.status) {
                        case 301:
                        case 302:
                            window.location.href = response.responseText
                            break
                    }
                }
            },
            error: function ( response ) {
                //TODO: custom fail function
                alert(method.toUpperCase() + ' ' + url + '   ' + response.status + ' ' + response.statusText + '\n' + response.responseText)
            },
            complete: function ( response ) {
                //TODO: custom complete function
            }
        })

        if (e.isDefaultPrevented()) return
    }


    // ALERT PLUGIN DEFINITION
    // =======================

    var old = $.fn.ajax

    $.fn.ajax = function (option) {
    return this.each(function () {
      var $this = $(this)
      var data  = $this.data('ajax')

      if (!data) $this.data('ajax', (data = new Alert(this)))
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

    $(document).on('click.ajax.data-api', dismiss, Ajax.prototype.ajax)

}(jQuery);