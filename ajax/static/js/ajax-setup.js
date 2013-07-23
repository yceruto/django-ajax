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

function ajax(method, url, data, onsuccess) {
    method(url, data, function(result){
        if (result.success) {
            if (onsuccess)
                onsuccess(result)
        } else
            switch (result.status) {
                case 500:
                    alert('Exception! ' + result.exception);
                    break;
                case 405:
                    alert('Method "' + result.method + '" not allowed! Only allow: "' + result.allow + '"');
                    break;
                case 301:
                case 302:
                    window.location.href = result.location;
                    break;
            }
    })
}

function post(url, data, onsuccess) {
    ajax($.post, url, data, onsuccess)
}

function get(url, data, onsuccess) {
    ajax($.get, url, data, onsuccess)
}

$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
