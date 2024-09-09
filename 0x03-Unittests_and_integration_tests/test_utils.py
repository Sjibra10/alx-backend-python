#!/usr/bin/env python3
"""Module"""

import unittest
from typing import Any
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """Class that inherits from unittest.TestCase"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected_output):
        """Testing function"""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected_output)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b')
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_exception_message):
        """Testing function"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
            self.assertEqual(context.exception, expected_exception_message)


class TestGetJson(unittest.TestCase):
    """Class to test get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """Test for get_json"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        with patch('utils.requests.get', return_value=mock_response):
            result = get_json(test_url)
            self.assertEqual(result, test_payload)
            mock_response.json.assert_called_once()


class TestMemoize(unittest.TestCase):
    """Class to test memoize"""

    def test_memoize(self):
        """Method to test memoize"""
        class TestClass:
            """Class"""
            def a_method(self):
                """Method"""
                return 42

            @memoize
            def a_property(self):
                """Method"""
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            test_instance = TestClass()
            result1 = test_instance.a_property
            result2 = test_instance.a_property
            mock_method.assert_called_once()
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
