#-*- coding: utf-8 -*-

from os import chdir, getcwd, listdir
from os.path import dirname, exists, join
from photorenamer import get_datime_original_fmt, InvalidPathError, photo_renamer
from pytest import raises
from shutil import copytree, rmtree
from tempfile import gettempdir

TEMP_PATH = join(gettempdir(), 'photorenamer')


def setup_module(module):
    if not exists(TEMP_PATH):
        copytree(join(dirname(__file__), '../img'), TEMP_PATH)
    photo_renamer(TEMP_PATH)


def teardown_module(module):
    if exists(TEMP_PATH):
        rmtree(TEMP_PATH)


def test_path_is_valid():
    with raises(InvalidPathError):
        photo_renamer(TEMP_PATH + '-foo')


def test_path_not_provided_must_scan_current_dir():
    curr_dir = getcwd()
    chdir(TEMP_PATH)
    new_dir = getcwd()

    photo_renamer()
    assert curr_dir != new_dir


def test_filename_is_equal_datetime_original():
    file_path = join(TEMP_PATH, listdir(TEMP_PATH)[0])
    datetime_original_fmt = get_datime_original_fmt(file_path)
    assert datetime_original_fmt == file_path.split('/')[-1]
