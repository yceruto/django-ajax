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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

function _ajax(method, url, data, onsuccess, onfail, onredirect) {
    method(url, data, function(result){
        if (result.status == 200) {
            if (onsuccess)
                onsuccess(result)
        } else {
            var message;

            switch (result.status) {
                case 500:
                    message = result.exception;
                    break;
                case 405:
                    message = result.method + ' ' + result.path;
                    break;
                case 410:
                case 404:
                case 403:
                case 400:
                case 304:
                    message = result.path;
                    break;
                case 301:
                case 302:
                    if (onredirect)
                        onredirect(result.status, result.path, result.location);
                    else
                        window.location.href = result.location;
                    break;
                default:
                    message = 'An unknown error has occurred.';
                    break;
            }

            if (onfail)
                onfail(result.status, result.status_text, message);
            else
                alert(result.status + ' ' + result.status_text + ' - ' + message);
        }
    })
}

function ajax_post(url, data, onsuccess, onfail, onredirect) {
    _ajax($.post, url, data, onsuccess, onfail, onredirect)
}

function ajax_get(url, data, onsuccess, onfail, onredirect) {
    _ajax($.get, url, data, onsuccess, onfail, onredirect)
}
