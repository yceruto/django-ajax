/* ========================================================================
 * Django Ajax: jquery.ajax.js v1.0
 * https://github.com/yceruto/django-ajax/
 * Copyright 2014 Yonel Ceruto Glez
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

var csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    crossDomain: false // obviates need for sameOrigin test
});

var ajax = function (url, options) {
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

    if (!$.isPlainObject(options))
        options = {};

    options = $.extend({}, ajax.DEFAULTS, options);

    $.ajax({
        url: url,
        type: options.method || 'get',
        data: options.data,
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }

            if (options.onBeforeSend && $.isFunction(options.onBeforeSend))
                options.onBeforeSend(xhr, settings);
        },
        success: function( response ){
            if (response.status == 200) {
                if (options.onSuccess && $.isFunction(options.onSuccess))
                    options.onSuccess(response.content);
                else
                    alert(response.content)
            } else {
                switch (response.status) {
                    case 301:
                    case 302:
                        if (options.onRedirect && $.isFunction(options.onRedirect))
                            options.onRedirect(response.content);
                        else
                            window.location.href = response.content;
                        break;
                    default:
                        if (options.onError && $.isFunction(options.onError))
                            options.onError(response);
                        else
                            alert(options.method.toUpperCase() + ' ' + url + '   ' + response.status + ' ' + response.statusText + '\n' + response.content);
                        break;
                }
            }
        },
        error: function(response) {
            if (options.onError && $.isFunction(options.onError))
                options.onError(response);
            else
                alert(options.method.toUpperCase() + ' ' + url + '   ' + response.status + ' ' + response.statusText + '\n' + response.content)
        },
        complete: function(response) {
            if (options.onComplete && $.isFunction(options.onComplete))
                options.onComplete(response);
        }
    })
};

ajax.DEFAULTS = {
    onSuccess: null,
    onError: null,
    onBeforeSend: null,
    onComplete: null,
    onRedirect: null
};

function ajaxPost(url, options) {
    options = $.extend({}, ajax.DEFAULTS, options, {method: 'post'});
    ajax(url, options)
}

function ajaxGet(url, options) {
    options = $.extend({}, ajax.DEFAULTS, options, {method: 'get'});
    ajax(url, options)
}