#!/usr/bin/env python3

"""csv2vcfmerge.py: Merge vcf and csv files into a single file for easy post processing."""

import os
import glob
import errno
import argparse
import pathlib
from functools import reduce
from utils import ngsutils, pdutils, vcfutils


def setup_args():
    parser = argparse.ArgumentParser(description='Merge csv or vcf files.')

    parser.add_argument('-c', action='store', dest='csv_file', help='CSV file', required=True)
    parser.add_argument('-v', action='store', dest='vcf_file', help='VCF file', required=True)
    parser.add_argument('-o', action='store', dest='out_filename', default='output.csv',
                        help='Output file name: default filename \'output.csv\'')
    parser.add_argument('-a', action='store_true', dest='all_vcf_columns', default=False,
                        help='Get additional vcf columns apart from the default ones')
    parser.add_argument('-m', action='append', dest='join_columns', default=[],
                        help='Columns to merge data', required=True)
    parser.add_argument('-j', action='store', dest='join_type', default='outer',
                        help='Join data: outer, inner, left or right. Default join type is \'outer\' join')
    parser.add_argument('-s', action='append', dest='sort_columns', help='Sort data by column')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')

    return parser.parse_args()


def load_and_merge(args):
    data_frames = []

    # read vcf file and append to data_frames list
    data_frames.append(vcfutils.read_vcf(args.vcf_file, args.all_vcf_columns))
    # read csv file and append to data_frames list
    data_frames.append(pdutils.load_csv_in_dataframe(args.csv_file))

    # if both were read successfully, begin merging process
    if (data_frames[0] is not None and data_frames[1] is not None):
        merged_file = ngsutils.merge_ngs_files(
            data_frames, args.join_columns, args.join_type, ['chr', 'Chr', 'CHR'], args.sort_columns)
        return pdutils.save_file_to_disk(merged_file, args.out_filename)
    else:
        return errno.EIO


# Gather our code in a main() function
def main():
    args = setup_args()
    print('Merging ' + args.vcf_file + " and " + args.csv_file)

    if (load_and_merge(args) == 0):
        print('Merging ready!!')
    else:
        print('Program error')


if __name__ == '__main__':
    main()
