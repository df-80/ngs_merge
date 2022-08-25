#!/usr/bin/env python3

"""osutils.py: Generic utility multi-platform functions."""

import os
import glob
import psutil
import shutil


def get_cpu_count():
    return psutil.cpu_count(logical=False)


def get_memory():
    return psutil.virtual_memory()


def get_total_filesize(files):
    total = 0
    for fp in files:
        total += os.path.getsize(fp)

    return total


def format_bytes(size_in_bytes):
    """Return the given bytes as a human-readable string"""
    B = size_in_bytes
    KB = 2 ** 10  # 1,024
    MB = KB ** 2  # 1,048,576
    GB = KB ** 3  # 1,073,741,824
    TB = KB ** 4  # 1,099,511,627,776

    if size_in_bytes < KB:
        return '{0}B'.format(B)
    elif KB <= size_in_bytes < MB:
        return '{0:.2f}KB'.format(B/KB)
    elif MB <= size_in_bytes < GB:
        return '{0:.2f}MB'.format(B/MB)
    elif GB <= size_in_bytes < TB:
        return '{0:.2f}GB'.format(B/GB)
    else:
        return '{0:.2f}TB'.format(B/TB)


def create_dir(dir_name):
    # create directory
    try:
        os.makedirs(dir_name)
    except (OSError, IOError) as e:
        print('>>> create_dir: {0} - error: {1} <<<'.format(dir_name, os.strerror(e.errno)))
        return e.errno
    else:
        return 0


def delete_dir(dir_name):
    try:
        shutil.rmtree(dir_name)
        print('\'{0}\' directory deleted'.format(dir_name))
    except (OSError, IOError) as e:
        print('>>> delete_dir: {0} - error: {1} <<<'.format(dir_name, os.strerror(e.errno)))
        return e.errno
    else:
        return 0
