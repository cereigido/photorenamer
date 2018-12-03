# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from hashlib import md5
from os import getcwd, listdir, rename, stat
from os.path import basename, dirname, isdir, isfile, join, splitext
from re import search
from photorenamer.exceptions import InvalidPathError
from PIL import Image
from PIL.ExifTags import TAGS

ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png',)

def get_exif_value(path, tag):
    exif = _get_exif(path)
    return datetime.strptime(exif[tag], '%Y:%m:%d %H:%M:%S') if tag in exif else None

def is_ready_to_rename(path):
    if not isfile(path):
        raise InvalidPathError()
    return not is_valid_filename(path) and is_valid_extension(path)

def is_valid_extension(path):
    return splitext(path)[-1].lower() in ALLOWED_EXTENSIONS

def is_valid_filename(filename):
    valid_format = search(r'^\d{8}-\d{6}-\w{4}.\w{3}$', filename) is not None
    return valid_format and is_valid_extension(filename)

def list_files(path):
    files = listdir(_get_root_path(path))
    files.sort()
    return files

def rename_file(path, add_seconds):
    file_date = get_exif_value(path, 'DateTimeOriginal') or datetime.fromtimestamp(stat(path).st_mtime)
    if file_date is not None:
        file_date += timedelta(seconds=add_seconds)

    new_path = join(dirname(path), _get_new_image_name(path, file_date))
    print('%s -> %s' % (basename(path), basename(new_path)))
    rename(path, new_path)

def _get_exif(path):
    ret = {}
    if is_ready_to_rename(path):
        i = Image.open(path)
        info = i._getexif() or {}
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value

    return ret  

def _get_new_image_name(path, file_date):
    checksum = _get_image_checksum(path)[:4]
    ext = splitext(path)[-1].lower()
    if path.find('/IMG-') > 0:
        return '%s-000000-%s%s' % (path[-19:-11], checksum, ext)
    elif file_date is not None:
        datetime_fmt = file_date.strftime('%Y%m%d-%H%M%S')
        return '%s-%s%s' % (datetime_fmt, checksum, ext)
    return '_%s-%s' % (checksum, basename(path))
 
def _get_image_checksum(path):
    if is_ready_to_rename(path):
        # using Image.open instead of open ignores different exif
        return md5(Image.open(path).tobytes()).hexdigest()
    return None

def _get_root_path(path=None):
    if not path:
        return getcwd()
    elif not isdir(path):
        raise InvalidPathError()
    return path
