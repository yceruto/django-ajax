# -*- coding: utf-8 -*-
"""
Mixin Response
"""

from django_ajax.decorators import ajax


class AJAXMixin(object):
    """
    AJAX Mixin Class
    """
    ajax_mandatory = True

    def dispatch(self, request, *args, **kwargs):
        """
        Using ajax decorator
        """
        return ajax(mandatory=self.ajax_mandatory)(super(
            AJAXMixin, self).dispatch)(request, *args, **kwargs)
