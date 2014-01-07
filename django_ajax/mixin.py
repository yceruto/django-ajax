"""
Ajax mixin
"""
from django_ajax.decorators import ajax


class AJAXResponseMixin(object):
    """
    AJAX Mixin
    """
    ajax_mandatory = True

    def dispatch(self, request, *args, **kwargs):
        """
        Using ajax decorator
        """
        return ajax(mandatory=self.ajax_mandatory)(
            super(AJAXResponseMixin, self).dispatch
        )(request, *args, **kwargs)
