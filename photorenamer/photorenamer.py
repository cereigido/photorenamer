#!/usr/bin/env python
#-*- coding: utf-8 -*-

from argparse import ArgumentParser
from datetime import datetime
from os import getcwd, listdir, rename
from os.path import getctime, getsize, isdir, isfile, join
from PIL import Image
from PIL.ExifTags import TAGS
import pexif


class InvalidPathError(Exception):
    pass


def get_datime_original_fmt(path):
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
    return datetime_fmt + ext


def get_exif(path):
    ret = {}
    i = Image.open(path)
    info = i._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value

    return ret


def photo_renamer(path=None):
    if not path:
        path = getcwd()
    elif not isdir(path):
        raise InvalidPathError()

    print '\nRenaming photos from %s' % path
    files = listdir(path)
    files.sort()

    for filename in files:
        cont_aux = 1
        if 'jpg' in filename.lower() or 'jpeg' in filename.lower():
            old_file_path = join(path, filename)
            new_filename = get_datime_original_fmt(old_file_path)
            new_file_path = join(path, new_filename)

            if not isfile(new_file_path) or getsize(old_file_path) != getsize(new_file_path):
                if isfile(new_file_path):
                    aux = ('000%s' % cont_aux)[-3:]
                    new_file_path = new_file_path.replace('.', '-%s.' % aux)
                    cont_aux += 1
                else:
                    cont_aux = 1

                if not isfile(new_file_path) or getsize(old_file_path) != getsize(new_file_path):
                    print '%s -> %s' % (filename, new_filename)
                    rename(old_file_path, new_file_path)


def main():
    parser = ArgumentParser()
    parser.add_argument('-p', '--path', dest='path', help='Path containing images to be renamed', required=False)
    args = parser.parse_args()
    photo_renamer(args.path)


if __name__ == '__main__':
    main()
