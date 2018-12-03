# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from mock import patch
from os import getcwd
from photorenamer import main, parse_args
from photorenamer.exceptions import InvalidPathError
from unittest import TestCase


class MainTestCase(TestCase):
    def test_main_should_raise_invalid_path_error_when_path_is_not_a_folder(self):
        with self.assertRaises(InvalidPathError):
            parse_args(['--path', '/this-is-an-invalid-folder'])

    def test_main_should_raise_invalid_path_error_when_path_is_a_file(self):
        with self.assertRaises(InvalidPathError):
            parse_args(['--path', './__init__.py'])

    # def test_get_checksum_should_raise_invalid_path_error_when_path_is_not_a_file(self):
    #     with self.assertRaises(InvalidPathError):
    #         get_checksum('invalid-path')

    # def test_get_checksum_should_return_string(self):
    #     checksum = get_checksum('/Users/cereigido/Downloads/pinguim.jpg')     
    #     self.assertEqual(type(checksum), str)
    #     self.assertEqual(len(checksum), 32)

    # def test_get_work_path_should_raise_invalid_path_error_when_invalid_path_is_provided(self):
    #     with self.assertRaises(InvalidPathError):
    #         get_work_path('invalid-path')

    # def test_get_work_path_should_return_current_path_when_no_path_is_provided(self):
    #     self.assertEqual(get_work_path(None), getcwd())
