from shortcuts import render_to_json
from response import JsonHttpResponse
from django.utils.unittest import TestCase

DEBUG = True
DEFAULT_CHARSET = 'utf-8'
SECRET_KEY = 'secret-key'


class ResponseTestCase(TestCase):
    """
    Response TestCase
    """
    def test_json_response(self):
        """
        test http json response
        """
        data = {'test': True}
        response = JsonHttpResponse(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.content, '{"test": true}')