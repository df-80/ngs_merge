#!/usr/bin/env python3

"""vcfutils.py: VCF utility functions."""

# allel is part of scikit-allel
import allel
import os
from utils import osutils


def read_vcf(fp, all_columns):
    try:
        print('Reading file ' + fp + ' - size: ' + str(osutils.format_bytes(os.path.getsize(fp))))
        if (all_columns):
            df = allel.vcf_to_dataframe(fp, fields='*', alt_number=1)
        else:
            df = allel.vcf_to_dataframe(fp)
        # Possible other similar fields are 'REF':'Ref', 'ALT':'Obs'
        df.rename(columns={'CHROM': 'Chr', 'POS': 'Start'}, inplace=True)

        return df
    except (OSError, IOError) as e:
        print('>>> read_vcf: {0} - error: {1} <<<'.format(fp, os.strerror(e.errno)))
        return None
    # except RuntimeError:
    #     print('>>> read_vcf: {0} - error: {1} <<<'.format(fp, 'Runtime error encountered'))
    #     return None
