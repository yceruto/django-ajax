/* ========================================================================
 * Django Ajax v2.2.10
 * https://github.com/yceruto/django-ajax/
 * Copyright 2014 Abalt
 * ======================================================================== */

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

$.ajaxSetup({
    crossDomain: false // obviates need for sameOrigin test
});

var ajax = function (url, options) {
    // If url is an object, simulate pre-1.5 signature
    if ( typeof url === "object" ) {
        options = url;
        url = options.url;
    }

    // Force options to be an object
    if (!$.isPlainObject(options))
        options = {};

    options = $.extend({}, ajax.DEFAULTS, options);

    var
        onSuccess = $.isFunction(options.onSuccess) ? options.onSuccess : ajax.DEFAULTS['onSuccess'],
        onRedirect = $.isFunction(options.onRedirect) ? options.onRedirect : ajax.DEFAULTS['onRedirect'],
        onError = $.isFunction(options.onError) ? options.onError : ajax.DEFAULTS['onError'],
        onComplete = $.isFunction(options.onComplete) ? options.onComplete : ajax.DEFAULTS['onComplete'],
        onBeforeSend = $.isFunction(options.onBeforeSend) ? options.onBeforeSend : ajax.DEFAULTS['onBeforeSend'];

    $.ajax({
        url: url,
        type: options.method || 'get',
        data: options.data,
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }

            onBeforeSend && onBeforeSend(xhr, settings);
        },
        success: function( response ){
            switch (response.status) {
                case 200:
                    options['process-fragments'] && response.content && process_fragments(response.content);

                    onSuccess && onSuccess(response);
                    break;
                case 301:
                case 302:
                    if (onRedirect)
                        onRedirect(response.content); //location
                    else
                        window.location.href = response.content;
                    break;
                default:
                    if (onError)
                        onError(response);
                    else
                        alert(options.method.toUpperCase() + ' ' + url + '   ' + response.status + ' ' + response.statusText + '\n' + response.content);
                    break;
            }
        },
        error: function(response) {
            if (onError)
                onError(response);
            else
                alert(options.method.toUpperCase() + ' ' + url + '   ' + response.status + ' ' + response.statusText + '\n' + response.content)
        },
        complete: function(response) {
            onComplete && onComplete(response);
        }
    });

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

    function process_fragments(content) {
        //process fragments
        if (content.fragments) {
            for (var s in content.fragments) {
                $(s).replaceWith(content.fragments[s])
            }
        }

        if (content['inner-fragments']) {
            for (var i in content['inner-fragments']) {
                $(i).html(content['inner-fragments'][i])
            }
        }

        if (content['append-fragments']) {
            for (var a in content['append-fragments']) {
                $(a).append(content['append-fragments'][a])
            }
        }

        if (content['prepend-fragments']) {
            for (var p in content['prepend-fragments']) {
                $(p).prepend(content['prepend-fragments'][p])
            }
        }
    }
};

ajax.DEFAULTS = {
    "process-fragments": true,
    onSuccess: null,
    onError: null,
    onBeforeSend: null,
    onComplete: null,
    onRedirect: null
};

/**
 * Ajax Method
 *
 * @param {String} method
 * @param {String} url
 * @param {Null|Object|Function} data
 * @param {Null|Object|Function} onSuccess
 * @param {Object} options
 */
function ajaxMethod(method, url, data, onSuccess, options) {
    if ($.isFunction(data)) {
        if ($.isPlainObject(onSuccess)) {
            options = onSuccess;
        }

        onSuccess = data;
        data = null;
    }

    options = $.extend({}, options, {
        url: url,
        method: method,
        data: data,
        onSuccess: function(response){
            $.isFunction(onSuccess) && onSuccess(response.content);
        }
    });
    ajax(options);
}

/**
 * Ajax Post Method
 *
 * @param {String} url
 * @param {Null|Object|Function} data
 * @param {Null|Object|Function} onSuccess
 * @param {Object} options
 */
function ajaxPost(url, data, onSuccess, options) {
    ajaxMethod('post', url, data, onSuccess, options);
}

/**
 * Ajax Get Method
 *
 * @param {String} url
 * @param {Null|Object|Function} data
 * @param {Null|Object|Function} onSuccess
 * @param {Object} options
 */
function ajaxGet(url, data, onSuccess, options) {
    ajaxMethod('get', url, data, onSuccess, options);
}
