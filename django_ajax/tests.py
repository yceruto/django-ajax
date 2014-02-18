"""
Tests
"""
from __future__ import unicode_literals

from django.utils.unittest import TestCase

from django_ajax.response import JSONResponse

DEBUG = True
DEFAULT_CHARSET = 'utf-8'
SECRET_KEY = 'j&^s-a4(uwj!fdqwr!_pa_0@#$kv8!4j(t3st44_6o^)g=ec%@'


class ResponseTestCase(TestCase):
    """
    Response TestCase
    """
    def test_json_response(self):
        """
        test http json response
        """
        data = {'test': True}
        response = JSONResponse(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.content, '{"test": true}')