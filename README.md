# ngs_merge

A python tool to merge Next Generation Sequencing (NGS) CSV output files into one CSV output file for easier post-processing of data.

## Overview:

The purpose of this application is to merge genetic variant files (SNP, InDel and SV) into a single file, with the possibility to split the 
file into several files by chromosome to be easily loaded in Excel.

## Requirements:
### Recommended system requirements:
* Dual Core CPU
* 16 GB RAM (Depending on amount of files to merge)

### Python requirements
* Python 3.7, 3.8, 3.9 -- see http://www.python.org

### Python dependencies
* pandas
* psutil
* scikit-allel library (for csv2vcfmerge.py only)

## Command line arguments
* -d: Directory where csv files are present e.g. '-d csv_directory/'.
* -o: Output filename. If this option is not given, the default output filename is 'output.csv'.
* -w: wildcard filenames, e.g. '-w *.sv.annot.csv' or '-w *.annot.csv' or '-w *.csv'.
* -c: Join data according to one column or more e.g. '-cChr -cStart'.
* -j: Join type e.g. '-jouter', '-jleft', etc. Default join is 'outer' join which retains all data.
* -s: Sort data according to one column or more e.g. '-sChr -sStart'.
* -b: Split files according to chromosomes and save files.
* -e: Erase all temporary directories created.

## Input
The input to this tool is a directory with a number of SNP, InDel or SV CSV files to merge.

## Output
The output is a single file containing all the variants present in the files merged.

## Example usage:

> csvmerge -d csv_files_directory/ -o result.csv -w *.annot.csv -cChr -cStart -jouter -sChr -sStart
> 
> csvmerge -d csv_files_directory/ -w *.indel.annot.csv -cChr -cStart -jouter -sChr -sStart -b
> 
> csvmerge -d csv_files_directory/ -o result.csv -w *.sv.annot.csv -cChr -cStart -jouter -sChr -sStart -b -e