from unittest import mock, TestCase
import pytest

class Testtest(TestCase):
    def setUp(self):
        self.attribute = 'Something'
        
    def test_something(self):
        my_value = self.attribute
        self.assertEqual(my_value, self.attribute)
