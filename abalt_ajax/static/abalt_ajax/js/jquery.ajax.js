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

+function ($) { "use strict";

  // AJAX SETUP
  // ======================

  $.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    }
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
    var url = $this.attr('href')
    var data = $this.attr('data-data')

    method = method ? method.toLowerCase() : 'get'

    url = url && url.replace(/.*(?=#[^\s]*$)/, '') // strip for ie7

    if (e) e.preventDefault()

    $.ajax({
      url: url,
      type: method,
      data: data, //TODO: serialize json data
      success: function(result){
        if (result.status == 200) {
          //TODO: fire onsuccess
          alert(result.content)
        } else {
          alert(method.toUpperCase() + ' ' + url + '\n' + result.status + ' ' + result.status_text + '\n' + result.content)

          switch (result.status) {
            case 301:
            case 302:
              window.location.href = result.content
              break
          }
        }
      }
    })

    if (e.isDefaultPrevented()) return
  }

  //TODO: plugins

  // ALERT DATA-API
  // ==============

  $(document).on('click.ajax.data-api', dismiss, Ajax.prototype.ajax)

}(jQuery);