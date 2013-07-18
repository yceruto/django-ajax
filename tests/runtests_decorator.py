from django.test import TestCase


class DecoratorTestCase(TestCase):
    def test(self):
        """
        test
        """
        self.assertEqual(1 + 1, 2)