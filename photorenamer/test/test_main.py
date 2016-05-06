# -*- coding: utf-8 -*-

from mock import patch
from os import getcwd
from photorenamer import main, get_checksum, get_work_path
from photorenamer.exceptions import InvalidPathError
from unittest import TestCase


class MainTestCase(TestCase):
    def test_get_checksum_should_raise_invalid_path_error_when_path_is_not_a_file(self):
        with self.assertRaises(InvalidPathError):
            get_checksum('invalid-path')

    def test_get_checksum_should_return_string(self):
        checksum = get_checksum('/Users/cereigido/Downloads/pinguim.jpg')
        self.assertEqual(type(checksum), str)
        self.assertEqual(len(checksum), 32)

    def test_get_work_path_should_raise_invalid_path_error_when_invalid_path_is_provided(self):
        with self.assertRaises(InvalidPathError):
            get_work_path('invalid-path')

    def test_get_work_path_should_return_current_path_when_no_path_is_provided(self):
        self.assertEqual(get_work_path(None), getcwd())
