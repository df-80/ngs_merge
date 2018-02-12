#!/usr/bin/env python3

"""csvmerge.py: Merge multiple csv files in a directory into a single file for easy post processing."""

import os
import glob
import errno
import argparse
from utils import futils, ngsutils, osutils, pdutils
from concurrent.futures import ThreadPoolExecutor, wait


def setup_args():
    parser = argparse.ArgumentParser(description='Merge compressed (*.gz) or uncompressed csv files.')

    parser.add_argument(
        '-d', action='store', dest='directory', help='Directory path where files are stored', required=True)
    parser.add_argument(
        '-w', action='store', dest='file_wildcard', help='Input file name wildcard: e.g. *.csv or *.csv.gz')
    parser.add_argument(
        '-o', action='store', dest='out_filename', help='Output file name: default filename \'output.csv\'')
    parser.add_argument(
        '-c', action='append', dest='join_columns', default=[], help='Columns to join data', required=True)
    parser.add_argument(
        '-j', action='store', dest='join_type', help='Join data: outer, inner, left or right. Default join type is \'outer\' join')
    parser.add_argument(
        '-s', action='append', dest='sort_columns', help='Sort data by column')
    parser.add_argument(
        '-b', action='store_true', dest='split_chromo', default=False, help='Split according to chromosones and save files')
    parser.add_argument(
        '-e', action='store_true', dest='erase_dirs', default=False, help='Erase all temporary directories created')

    parser.add_argument('--version', action='version', version='%(prog)s 0.2')

    return parser.parse_args()


def load_and_merge(args, files, chr_dir=None):
    data_frames = pdutils.load_files_in_dataframe(files)

    # Get join type to use when joining files. Default is 'outer' join.
    join_type = 'outer' if args.join_type is None else args.join_type
    # Get which columns to use for sorting data. Default is an empty list.
    sort_columns = [] if args.sort_columns is None else args.sort_columns
    # Save resulting merged file to disk.
    filename = args.out_filename if chr_dir is None else '.' + os.sep + 'merged' + os.sep + chr_dir + '.csv'

    merged_file = ngsutils.merge_ngs_files(
        data_frames, args.join_columns, join_type, ['chr', 'Chr', 'CHR'], sort_columns)

    return pdutils.save_file_to_disk(merged_file, filename)


def process_files_on_disk(args, files, cpu_count):
    result = ngsutils.delete_chromo_dirs(['split', 'merged'])
    if result != 0:
        print('Error: Error while deleting directories')
        return result

    result = ngsutils.create_chromo_dirs(['split', 'merged'])
    if result != 0 and result != errno.EEXIST:
        print('Error: Fatal error while creating directories')
        return result
    # split files according to chromosone
    result = ngsutils.split_files(files)
    if result != 0:
        return result
    # create threadpoolexecutor with cpu count
    pool = ThreadPoolExecutor(cpu_count)
    futures = []
    # loop into each split/chr* directory
    for chr_dir in ngsutils.chromo_dirs:
        print('Directory: split/' + chr_dir)
        files = glob.glob('./split/' + chr_dir + '/*.csv')
        futures.append(pool.submit(load_and_merge, args, files, chr_dir))
    # wait for all threads to be ready
    wait(futures)
    # append every chr file into one big file
    return ngsutils.save_chromos_in_one_file(args.out_filename)


# Gather our code in a main() function
def main():
    args = setup_args()
    print('Changing directory to ' + args.directory)

    # Some input validation
    if ((args.erase_dirs is True) and (args.split_chromo is True)):
        print('Invalid options: -b and -e options are mutually exclusive!')
        exit()

    try:
        os.chdir(args.directory)
    except IOError:
        print('Invalid directory: ' + args.directory)
        exit()

    # Read wild card argument. If absent, first try csv files then gz files.
    files = futils.get_files_to_process(args.file_wildcard)
    if (files is None):
        print('No suitable files found! Exiting program')
        exit()

    # Get machine cpu and memory stats
    cpu_count = osutils.get_cpu_count()
    mem_stats = osutils.get_memory()
    print('CPU count: {0}'.format(cpu_count))
    print('Memory stats: Total: {0}, Available: {1}, Free: {2}'.format(
        osutils.format_bytes(mem_stats.total),
        osutils.format_bytes(mem_stats.available),
        osutils.format_bytes(mem_stats.free)))
    # Get total file size to process
    files_size = osutils.get_total_filesize(files)
    print('Total files size to process: {0}'.format(osutils.format_bytes(files_size)))
    # Get all csv headers and intersecting headers
    csv_headers, intersect_headers = futils.get_csv_headers(files, ['', '.'])
    print('All csv headers: {0}'.format(csv_headers))
    print('Intersecting csv headers: {0}'.format(intersect_headers))

    # sort file order by filename so output columns order is according to filenames
    files.sort()

    # Decide how to handle execution, either in one chunk or split in multiple files
    if ((files_size < mem_stats.available/3) and (args.split_chromo is False)):
        result = load_and_merge(args, files)
    else:
        result = process_files_on_disk(args, files, cpu_count)
        # Check if split and merge directories should be deleted
        if args.erase_dirs is True:
            ngsutils.delete_chromo_dirs(['split', 'merged'])

    if result == 0:
        print('Merge ready!!!')
    elif result == errno.ENOSPC:
        print('Error: No space left on device.')
    else:
        print('Error: errno {0} occured.'.format(result))

if __name__ == '__main__':
    main()
