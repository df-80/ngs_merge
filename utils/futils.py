#!/usr/bin/env python3

"""futils.py: File utility functions for csv files."""

import csv
import glob


def get_files_to_process(file_wildcard=None):
    ''' Read wild card argument. If absent, first try csv files then gz files'''
    if file_wildcard:
        files = glob.glob(file_wildcard)
    else:
        files = glob.glob('*.csv')
        if (len(files) == 0):
            files = glob.glob('*.csv.gz')

    if (len(files) == 0):
        return None
    else:
        return files


def get_csv_headers(files, filter_list=[]):
    '''Return a list of all csv headers and intersecting headers found in files'''
    headers = []
    intersecting_headers = []
    for fp in files:
        with open(fp, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            # concatenate lists
            headers += header
            # if intersect list is empty, concat lists otherwise take intersecting elements
            if (len(intersecting_headers) == 0):
                intersecting_headers += header
            else:
                list(set(intersecting_headers).intersection(header))

    # filter list from unwanted characters
    all_headers = [x for x in set(headers) if str.strip(x) not in filter_list]
    intersect_headers = [x for x in set(intersecting_headers) if str.strip(x) not in filter_list]

    return all_headers, intersect_headers
