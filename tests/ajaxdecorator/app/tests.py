from __future__ import unicode_literals
from datetime import datetime
from django.test import TestCase
from django_ajax.encoder import LazyJSONEncoder
import json


class LazyJSONEncoderMixinTestCase(TestCase):
    def test_default_date(self):
        data = {'datetime': datetime.today()}
        self.assertEqual('{"datetime": "' + data['datetime'].isoformat() + '"}', json.dumps(data, cls=LazyJSONEncoder))


class BaseTestCase(TestCase):
    def post(self, uri, data=None):
        response = resp = self.client.get(uri, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEquals(200, resp.status_code)
        self.assertEquals('application/json', response['Content-Type'])
        if isinstance(response.content, str):
            return response, json.loads(response.content)
        else:
            return response, json.loads(response.content.decode('utf-8'))


class FooTestCase(BaseTestCase):
    def test_json_response(self):
        resp, data = self.post('/ajax/foo')

        self.assertEqual('OK', data['statusText'])
        self.assertEqual({'foo': True}, data['content'])


class LoginRequiredTestCase(BaseTestCase):
    def test_json_response(self):
        resp, data = self.post('/ajax/login-required')

        self.assertEquals(302, data['status'])
        self.assertEqual('FOUND', data['statusText'])


class RenderTestCase(BaseTestCase):
    def test_json_response(self):
        resp, data = self.post('/ajax/render')

        self.assertEquals(200, data['status'])
        self.assertEqual('OK', data['statusText'])
        self.assertEqual('<html>Hello</html>', data['content'].strip())


class RenderClassBasedViewTestCase(BaseTestCase):
    def test_json_response(self):
        resp, data = self.post('/ajax/render-class-based-view')

        self.assertEquals(200, data['status'])
        self.assertEqual('OK', data['statusText'])
        self.assertEqual('<html>Hello</html>', data['content'].strip())


class ExceptionTestCase(BaseTestCase):
    def test_json_response(self):
        resp, data = self.post('/ajax/exception')

        # self.assertEquals(200, data['status'])
        self.assertEqual('INTERNAL SERVER ERROR', data['statusText'])


class RaiseExceptionTestCase(BaseTestCase):
    def test_json_response(self):
        resp, data = self.post('/ajax/raise-exception')

        # self.assertEquals(200, data['status'])
        self.assertEqual('NOT FOUND', data['statusText'])
