#!/usr/bin/env python
#-*- coding: utf-8 -*-

from argparse import ArgumentParser
from datetime import datetime
from hashlib import md5
from os import getcwd, listdir, rename
from os.path import getctime, getsize, isdir, isfile, join
from PIL import Image
from PIL.ExifTags import TAGS
import pexif

args = None
INFO = 1
DEBUG = 2
ALLOWED_EXTENSIONS = ('jpg', 'jpeg', 'png')

class InvalidPathError(Exception):
    pass


def get_exif(path):
    ret = {}
    i = Image.open(path)
    info = i._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value

    return ret


def get_checksum(path):
    return md5(open(path, 'rb').read()).hexdigest()


def get_new_file_name(path):
    i = Image.open(path)
    info = get_exif(path)

    if not 'DateTimeOriginal' in info:
        i2 = pexif.JpegFile.fromFile(path)
        dt = str(datetime.fromtimestamp(getctime(path))).replace('-', ':')
        i2.exif.primary.ExtendedEXIF.DateTime = dt
        i2.exif.primary.ExtendedEXIF.DateTimeOriginal = dt
        i2.writeFile(path)
        info = get_exif(path)

    datetime_fmt = info.get('DateTimeOriginal').replace(':', '').replace(' ', '-')
    ext = path[path.rindex('.'):].lower()
    return '%s-%s%s' % (datetime_fmt, get_checksum(path)[:4], ext)


def photo_renamer():
    path = args.path
    if not path:
        path = getcwd()
    elif not isdir(path):
        raise InvalidPathError()

    log(INFO, 'Renaming photos from %s' % path)
    files = listdir(path)
    files.sort()
    renamed = 0

    for filename in files:
        if filename.lower().split('.')[-1] in ALLOWED_EXTENSIONS:
            old_file_path = join(path, filename)
            new_filename = get_new_file_name(old_file_path)
            new_file_path = join(path, new_filename)

            if not isfile(new_file_path):
                log(DEBUG, '%s -> %s' % (filename, new_filename))
                rename(old_file_path, new_file_path)
                renamed += 1
            else:
                log(DEBUG, '%s already exists' % new_filename)

    log(DEBUG, '%s files renamed' % renamed)


def log(log_level, msg):
    if log_level == INFO or args.verbose:
        print msg


def main():
    parser = ArgumentParser()
    parser.add_argument('-p', '--path', dest='path', help='Path containing images to be renamed', required=False)
    parser.add_argument('-v', '--verbose', dest='verbose', help='Verbose mode', action='store_true', default=False)
    
    global args
    args = parser.parse_args()
    photo_renamer()


if __name__ == '__main__':
    main()
