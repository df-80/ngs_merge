"""ngsutils.py: NGS-specific functions to read csv or vcf files."""

import os
import errno
import pandas as pd
from utils import osutils, pdutils

chromo_list = [
    'chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7',
    'chr8', 'chr9', 'chr10', 'chr11', 'chr12', 'chr13',
    'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19',
    'chr20', 'chr21', 'chr22', 'chrX', 'chrY', 'chrM']

chromo_dirs = [
    'chr01', 'chr02', 'chr03', 'chr04', 'chr05', 'chr06',
    'chr07', 'chr08', 'chr09', 'chr10', 'chr11', 'chr12',
    'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18',
    'chr19', 'chr20', 'chr21', 'chr22', 'chrX', 'chrY', 'chrM']


def create_chromo_dirs(dirs):
    # create directories where files will be split or merged in a single file
    for dir in dirs:
        result = osutils.create_dir(dir)
        if result != 0:
            print('>>> create_chromo_dirs: {0} - error: {1} <<<'.format(dir, os.strerror(result)))
            return result

    # create directories where files will be split according to chromosone
    for chr_dir in chromo_dirs:
        result = osutils.create_dir(dirs[0] + os.sep + chr_dir)
        if result != 0:
            print('>>> create_chromo_dirs: {0} - error: {1} <<<'.format(chr_dir, os.strerror(result)))
            return result

    return 0


def delete_chromo_dirs(dirs):
    for dir_name in dirs:
        result = osutils.delete_dir(dir_name)
        if result != 0 and result != errno.ENOENT:
            print('>>> delete_chromo_dirs: {0} - error: {1} <<<'.format(dir_name, os.strerror(result)))
            return result

    return 0


def split_files(files):
    try:
        for fp in files:
            df = pdutils.load_csv_in_dataframe(fp)
            # Split files according to chormosone
            for chr, chr_dir in zip(chromo_list, chromo_dirs):
                csv_chr = df[df['Chr'] == chr]
                csv_chr.to_csv('split' + os.sep + chr_dir + os.sep + os.path.splitext(fp)[0] +
                               '_' + chr_dir + '.csv', index=False)
    except (OSError, IOError) as e:
        print('>>> split_files: {0} - error: {1} <<<'.format(files, os.strerror(result)))
        return e.errno
    else:
        return 0


def save_chromos_in_one_file(output_filename='output.csv'):
    print('Writing merged result to ' + output_filename)
    out_fp = output_filename

    header_saved = False
    try:
        with open(out_fp, 'w') as fout:
            for chr_dir in chromo_dirs:
                with open('.' + os.sep + 'merged' + os.sep + chr_dir + '.csv') as fin:
                    header = next(fin)
                    if not header_saved:
                        fout.write(header)
                        header_saved = True
                    for line in fin:
                        fout.write(line)
    except (OSError, IOError) as e:
        return e.errno
    else:
        return 0


def merge_ngs_files(data_frames, join_columns, join_type, chr_name_list=[], sort_columns=[], sort_asc=True):
    df_merged = pdutils.merge_files(data_frames, join_columns, join_type)
    # check for chr in list of sort columns
    for chr_column in sort_columns:
        if chr_column in chr_name_list:
            # Remove chr from the chromosones to sort by number
            df_merged.Chr = df_merged.Chr.str[len(chr_column):]
            # change Chr column type to integer for sorting
            df_merged.Chr = df_merged.Chr.apply(pd.to_numeric, errors='ignore')
            break
    # Sort by sort_columns
    if sort_columns:
        print('Sort columns by \'' + ', '.join(sort_columns) + '\'')
        df_merged.sort_values(by=sort_columns, ascending=sort_asc, inplace=True)
    # put back the chr string infront of chromosome letter
    if any(i in chr_name_list for i in sort_columns):
        df_merged.Chr = df_merged.Chr.astype(str)
        df_merged.Chr = chr_column + df_merged.Chr
    # move join columns at the beginning of the table
    for col, i in zip(join_columns, list(range(len(join_columns)))):
        df_merged.insert(i, '_' + col + '_', df_merged[col])
        df_merged.pop(col)

    return df_merged
