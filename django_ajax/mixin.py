"""
Mixin Response
"""
from __future__ import unicode_literals

from django_ajax.decorators import ajax


class AJAXMixin(object):

    """
    AJAX Mixin Class
    """
    ajax_mandatory = True
    json_encoder = None

    def dispatch(self, request, *args, **kwargs):
        """
        Using ajax decorator
        """
        ajax_kwargs = {'mandatory': self.ajax_mandatory}
        if self.json_encoder:
            ajax_kwargs['cls'] = self.json_encoder

        return ajax(**ajax_kwargs)(super(
            AJAXMixin, self).dispatch)(request, *args, **kwargs)
