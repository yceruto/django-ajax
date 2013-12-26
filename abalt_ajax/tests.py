from django.utils.unittest import TestCase


class DecoratorTestCase(TestCase):
    """
    Decorator Test Case
    """
    def test(self):
        """
        test
        """
        self.assertEqual(1 + 1, 2)
