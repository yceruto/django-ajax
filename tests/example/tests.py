from __future__ import unicode_literals
from django.test import TestCase
from django_ajax.response import JSONResponse

class ResponseTestCase(TestCase):
    def test_json_response(self):
        data = {'test': True}
        response = JSONResponse(data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.content, '{"test": true}')
