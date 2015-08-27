#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from datetime import datetime
from exceptions import InvalidPathError
from hashlib import md5
from os import getcwd, listdir, remove, rename
from os.path import getctime, getsize, isdir, isfile, join
from PIL import Image
from PIL.ExifTags import TAGS

args = None
INFO = 1
DEBUG = 2
ALLOWED_EXTENSIONS = ('jpg', 'jpeg', 'png')


def get_checksum(path):
    if not isfile(path):
        raise InvalidPathError()

    # using Image.open instead of open makes different exif
    # data point to the same hase
    return md5(Image.open(path).tostring()).hexdigest()


def get_exif(path):
    ret = {}
    i = Image.open(path)
    info = i._getexif() or {}
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value

    return ret


def get_new_file_name(path):
    i = Image.open(path)
    info = get_exif(path)
    ext = path[path.rindex('.'):].lower()

    if 'DateTimeOriginal' not in info and args.use_ctime:
        i2 = pexif.JpegFile.fromFile(path)
        dt = str(datetime.fromtimestamp(getctime(path))).replace('-', ':')
        i2.exif.primary.ExtendedEXIF.DateTime = dt
        i2.exif.primary.ExtendedEXIF.DateTimeOriginal = dt
        i2.writeFile(path)
        info = get_exif(path)

    checksum = get_checksum(path)

    if 'DateTimeOriginal' in info:
        datetime_fmt = info.get('DateTimeOriginal').replace(':', '').replace(' ', '-')
        new_file_name = '%s-%s%s' % (datetime_fmt, checksum[:4], ext)
    else:
        new_file_name = '%s%s' % (checksum, ext)

    return new_file_name


def log(log_level, msg):
    if log_level == INFO or args.verbose:
        print msg


def main(args):
    path = args.path
    if not path:
        path = getcwd()
    elif not isdir(path):
        raise InvalidPathError()

    log(INFO, 'Renaming photos from %s' % path)
    files = listdir(path)
    files.sort()
    renamed = 0

    for file_name in files:
        if file_name.lower().split('.')[-1] in ALLOWED_EXTENSIONS:
            old_file_path = join(path, file_name)
            new_file_name = get_new_file_name(old_file_path)
            new_file_path = join(path, new_file_name)

            if file_name != new_file_name:
                if not isfile(new_file_path):
                    log(DEBUG, '%s -> %s' % (file_name, new_file_name))
                    rename(old_file_path, new_file_path)
                    renamed += 1
                else:
                    ui = raw_input('Cannot rename %s, target file %s already exists, remove source file? (Y/n) ' % (file_name, new_file_name)) or 'Y'
                    if ui.upper() == 'Y':
                        log(DEBUG, 'Removing file %s' % file_name)
                        remove(old_file_path)

    log(DEBUG, '%s files renamed' % renamed)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-p', '--path', dest='path', help='Path containing images to be renamed', required=False)
    parser.add_argument('-c', '--ctime', dest='use_ctime', help='If date tag is not available, use file creation time?', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', dest='verbose', help='Verbose mode', action='store_true', default=False)
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
