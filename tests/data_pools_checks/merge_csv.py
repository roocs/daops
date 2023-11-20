#/usr/bin/env python

import os
import argparse
from itertools import chain

from .results_db import ResultsDB


def remove_dups_from_sorted(lst):
    first = True
    for item in lst:
        if first or item != prev:
            first = False
            prev = item
            yield item
    

def merge_csv(infiles, outfile):

    all_files = infiles
    if os.path.exists(outfile):
        all_files.append(outfile)

    with ResultsDB(None, csvgz_file=all_files[0], read_only=True) as dbin:
        columns = dbin.columns

    rows = []
    for fn in all_files:
        with ResultsDB(columns, csvgz_file=fn, sqlite_file=None, read_only=True) as dbin:
            rows.extend(list(dbin.read_csvgz()))

    primary_index = columns.index('test_time')

    key_getter = lambda arr: \
        (arr[primary_index],) + tuple([arr[i] for i in range(len(arr)) if i != primary_index])
    
    rows.sort(key=key_getter)    

    with ResultsDB(columns, csvgz_file=outfile, sqlite_file=None) as dbout:
        dbout.write_csvgz(remove_dups_from_sorted(rows))


def _cli_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', 
                        help='output filename (may be pre-existing)',
                        required=True,
                        type=_csvgz_file,
                        nargs=1)
    parser.add_argument('input_files',
                        type=_existing_csvgz_file,
                        help='input filename(s)',
                        nargs='+')
    return parser.parse_args()


def _csvgz_file(path):
    if not path.endswith('.csv.gz'):
        raise argparse.ArgumentTypeError(f'filename {path} does not end .csv.gz')
    return path


def _existing_csvgz_file(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f'file {path} does not exist')
    return _csvgz_file(path)


def cli():
    args = _cli_arg_parser()
    out_file, = args.output
    print(f'Merging contents of files {args.input_files} into {out_file}')
    merge_csv(args.input_files, out_file)
    print('done')
