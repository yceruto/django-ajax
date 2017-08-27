from __future__ import unicode_literals
from django.test import TestCase
from django.utils import six
from django_ajax.response import JSONResponse

class ResponseTestCase(TestCase):
    def test_json_response(self):
        data = {'test': True}
        response = JSONResponse(data)

        self.assertEquals(200, response.status_code)
        self.assertEquals('application/json', response['Content-Type'])
        if isinstance(response.content, six.text_type):
            content = response.content
        else:
            content = response.content.decode('utf-8')
        self.assertEquals('{"test": true}', content)
