# -*- coding: utf-8 -*-

from datetime import datetime
from os import getcwd
from os.path import join
from shutil import copyfile
from tempfile import gettempdir
from unittest import TestCase
from mock import patch
from photorenamer.scanner import ALLOWED_EXTENSIONS, get_exif_value, get_new_filename_options, is_ready_to_rename, is_valid_extension, is_valid_filename, list_files, _get_exif, _get_image_checksum, _get_root_path
from photorenamer.exceptions import InvalidPathError

TEMP_DIR = gettempdir()
INVALID_FILENAME = 'this-is-invalid'
INVALID_FILENAME_EXTENSION = '19810915-114000-abcd.foo'
INVALID_FILENAME_WITH_ALLOWED_EXTENSION = 'foo%s' % ALLOWED_EXTENSIONS[0]
VALID_FILENAME = '19810915-114000-abcd%s' % ALLOWED_EXTENSIONS[0]

class ScannerTestCase(TestCase):
    def test_scanner_get_exif_should_raise_invalid_path_error_when_path_is_not_a_file(self):
        with self.assertRaises(InvalidPathError):
            _get_exif(INVALID_FILENAME_WITH_ALLOWED_EXTENSION)

    def test_scanner_get_exif_should_return_a_dict_when_valid_path_is_provided(self):
        filename = 'sample-1.jpg'
        path = join(gettempdir(), filename)
        copyfile(join(getcwd(), 'img', filename), path)
        self.assertIsInstance(_get_exif(path), dict)

    @patch('photorenamer.scanner._get_exif', return_value={'DateTime': '1981:09:15 11:40:00'})
    @patch('photorenamer.scanner._get_image_checksum', return_value='abcd')
    def test_scanner_get_exif_value_should_return_a_datetime_when_datetime_original_present_on_exif(self, *args):
        self.assertIsInstance(get_exif_value('mock-path', 'DateTime'), datetime)

    @patch('photorenamer.scanner._get_exif', return_value={})
    def test_scanner_get_exif_value_should_return_none_when_datetime_original_not_present_on_exif(self, *args):
        self.assertIsNone(get_exif_value('mock-path', 'DateTime'))

    def test_scanner_get_image_checksum_should_raise_invalid_path_error_when_path_is_not_a_file(self):
        with self.assertRaises(InvalidPathError):
            _get_image_checksum(INVALID_FILENAME_WITH_ALLOWED_EXTENSION)

    def test_scanner_get_image_checksum_should_checksum_when_image_is_provided(self):
        filename = 'sample-1.jpg'
        path = join(gettempdir(), filename)
        copyfile(join(getcwd(), 'img', filename), path)
        self.assertEqual(len(_get_image_checksum(path)), 32)

    def test_scanner_get_image_checksum_should_return_none_when_path_is_invalid(self):
        path = join(gettempdir(), INVALID_FILENAME_EXTENSION)
        temp_file = open(path, 'w')
        temp_file.close()
        self.assertIsNone(_get_image_checksum(path))

    @patch('photorenamer.scanner.get_exif_value', return_value='exif')
    @patch('photorenamer.scanner._get_atime', return_value=12345.0)
    @patch('photorenamer.scanner._get_ctime', return_value=12345.0)
    @patch('photorenamer.scanner._get_mtime', return_value=12345.0)
    @patch('photorenamer.scanner._get_image_checksum', return_value='abcd')
    @patch('photorenamer.scanner._get_new_image_name', return_value='new-image')
    def test_scanner_get_new_filename_options_should_return_a_list(self, *args):
        self.assertIsInstance(get_new_filename_options(VALID_FILENAME), list)

    def test_scanner_get_root_path_should_raise_invalid_path_error_when_path_is_not_a_folder(self):
        with self.assertRaises(InvalidPathError):
            _get_root_path(INVALID_FILENAME)

    def test_scanner_get_root_path_should_return_cwd_when_not_path_is_provided(self):
        self.assertEqual(getcwd(), _get_root_path())

    def test_scanner_get_root_path_should_return_path_when_path_is_a_folder(self):
        self.assertEqual(_get_root_path(TEMP_DIR), TEMP_DIR)

    def test_scanner_is_ready_to_rename_should_return_false_when_extension_is_not_allowed(self):
        path = join(gettempdir(), INVALID_FILENAME_EXTENSION)
        temp_file = open(path, 'w')
        temp_file.close()
        self.assertFalse(is_ready_to_rename(path))

    def test_scanner_is_ready_to_rename_should_return_true_when_extension_is_allowed(self):
        path = join(gettempdir(), INVALID_FILENAME_WITH_ALLOWED_EXTENSION)
        temp_file = open(path, 'w')
        temp_file.close()
        self.assertTrue(is_ready_to_rename(path))

    def test_scanner_is_valid_extension_should_return_false_when_extension_not_allowed(self):
        self.assertFalse(is_valid_extension(INVALID_FILENAME_EXTENSION))

    def test_scanner_is_valid_extension_should_return_true_when_extension_allowed(self):
        self.assertTrue(is_valid_extension(VALID_FILENAME))

    def test_scanner_is_valid_filename_should_return_false_when_extension_not_valid(self):
        self.assertFalse(is_valid_filename(INVALID_FILENAME_EXTENSION))

    def test_scanner_is_valid_filename_should_return_false_when_not_valid(self):
        self.assertFalse(is_valid_filename(INVALID_FILENAME))

    def test_scanner_is_valid_filename_should_return_true_when_valid(self):
        self.assertTrue(is_valid_filename(VALID_FILENAME))

    def test_scanner_list_files_should_return_a_list(self):
        self.assertIsInstance(list_files(TEMP_DIR), list)
