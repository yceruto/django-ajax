from django.test import TestCase
from django_ajax.response import JSONResponse

class ResponseTestCase(TestCase):
    def test_json_response(self):
        data = {'test': True}
        response = JSONResponse(data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response['Content-Type'], 'application/json')
        self.assertEquals(response.content, '{"test": true}')
