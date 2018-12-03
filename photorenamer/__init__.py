#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from __future__ import print
from argparse import ArgumentParser
from datetime import datetime, timedelta
from os import getcwd, listdir, remove
from os.path import getctime, getsize, isdir, isfile, join
from subprocess import check_output
from sys import argv
from PIL import Image   
from PIL.ExifTags import TAGS
from photorenamer.exceptions import InvalidPathError
from photorenamer.prompter import ask_change_valid_file, ask_new_filename
from photorenamer.scanner import is_valid_extension, is_valid_filename, list_files, rename_file


# def get_new_file_name(path):
#     if path.find('/IMG-') > 0:
#         new_file_name = '%s-000000-%s%s' % (path[-19:-11], checksum[:4], ext)
#     else:
#         new_file_name = '_%s%s' % (checksum, ext)

#     return new_file_name

# def main2():
    # for file_name in files:
    #     if file_name.lower().split('.')[-1] in ALLOWED_EXTENSIONS and not search('^\d{8}-\d{6}-\w{4}.\w{3}$', file_name):
    #         old_file_path = join(path, file_name)
    #         new_file_name = get_new_file_name(old_file_path)
    #         new_file_path = join(path, new_file_name)

    #         if file_name != new_file_name:
    #             if not isfile(new_file_path):
    #                 log(DEBUG, '%s -> %s' % (file_name, new_file_name))
    #                 rename(old_file_path, new_file_path)
    #                 renamed += 1
    #             else:
    #                 ui = raw_input('Cannot rename %s, target file %s already exists, remove source file? (Y/n) ' % (file_name, new_file_name)) or 'Y'
    #                 if ui.upper() == 'Y':
    #                     log(DEBUG, 'Removing file %s' % file_name)
    #                     remove(old_file_path)

    # log(DEBUG, '%s files renamed' % renamed)


def main():
    parsed_args = parse_args(argv[1:])
    path = parsed_args.path
    add_seconds = parsed_args.add_seconds

    for filename in list_files(path):
        full_path = join(path, filename)
        if is_valid_filename(filename):
            rename_file(full_path, add_seconds)
            pass
        elif is_valid_extension(full_path):
            rename_file(full_path, add_seconds)

def parse_args(payload):
    parser = ArgumentParser()
    parser.add_argument('--path', dest='path', help='Path containing images to be renamed', required=False)
    parser.add_argument('--add_seconds', dest='add_seconds', help='Seconds to add to image property', type=int, default=0)
    parsed_args = parser.parse_args(payload)

    if not isdir(parsed_args.path):
        raise InvalidPathError()
    elif isfile(parsed_args.path):
        raise InvalidPathError()

    return parsed_args
