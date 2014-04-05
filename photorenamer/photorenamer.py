#-*- coding: utf-8 -*-

from argparse import ArgumentParser
from os import getcwd, listdir, rename
from os.path import isdir, join
from PIL import Image
from PIL.ExifTags import TAGS


class InvalidPathError(Exception):
    pass


def get_datime_original_fmt(path):
    datetime_fmt = get_exif(path).get('DateTimeOriginal', '').replace(':', '').replace(' ', '-')
    ext = path[path.rindex('.'):].lower()
    return datetime_fmt + ext


def get_exif(path):
    ret = {}
    i = Image.open(path)
    info = i._getexif()
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
    for filename in listdir(path):
        if 'jpg' in filename.lower():
            file_path = join(path, filename)
            new_file = get_datime_original_fmt(file_path)
            if filename != new_file:
                print '%s -> %s' % (filename, new_file)
                rename(join(path, filename), join(path, new_file))


def main():
    parser = ArgumentParser()
    parser.add_argument('-p', '--path', dest='path', help='Path containing images to be renamed', required=False)
    args = parser.parse_args()
    photo_renamer(args.path)


if __name__ == '__main__':
    main()
