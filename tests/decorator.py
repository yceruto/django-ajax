from django.test import TestCase


class DecoratorTestCase(TestCase):
    def test(self):
        self.assertEqual(1 + 1, 2)