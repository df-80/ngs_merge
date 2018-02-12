#!/usr/bin/env python3

"""pdutils.py: Pandas utility functions."""

import os
import errno
import pathlib
import pandas as pd
from functools import reduce
from utils import osutils


def load_files_in_dataframe(files):
    data_frames = []

    try:
        for fp in files:
            df = load_csv_in_dataframe(fp)
            # append every df in a data_frames list
            data_frames.append(df)
    except (OSError, IOError, FileNotFoundError) as e:
        print('>>> load_files_in_dataframe: {0} <<<'.format(fp))
        return e.errno
    else:
        return data_frames


def load_csv_in_dataframe(fp):
    print('Reading file ' + fp + ' - size: ' + str(osutils.format_bytes(os.path.getsize(fp))))
    # read in the files (compressed or uncompressed) and put them into dataframes
    if (str.lower(pathlib.Path(fp).suffix) == '.csv'):
        return pd.read_csv(fp, sep=',')
    elif (str.lower(pathlib.Path(fp).suffix) == '.gz'):
        return pd.read_csv(fp, compression='gzip', sep=',')


def save_file_to_disk(merged_file, output_filename):
    try:
        if (output_filename):
            print('Writing file to ' + output_filename)
            merged_file.to_csv(output_filename, index=False)
        else:
            print('Writing file to output.csv')
            merged_file.to_csv('output.csv', index=False)
    except (OSError, IOError) as e:
        print('>>> save_file_to_disk: {0} <<<'.format(output_file))
        return e.errno
    else:
        return 0


def merge_files(data_frames, join_columns, join_type):
    print('Merge files on \'' + join_type + '\' join using \'' + ', '.join(join_columns) + '\' columns.')
    # merge all files using a join_type
    df_merged = reduce(lambda left, right: pd.merge(
        left, right, how=join_type, on=join_columns), data_frames).fillna('0')
    print('Files merged ...')

    return df_merged
