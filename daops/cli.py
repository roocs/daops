"""Console script for daops."""

__author__ = """Alan Iwi"""
__contact__ = 'alan.iwi@stfc.ac.uk'
__copyright__ = "Copyright 2023 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import argparse
import sys
import dateutil.parser

from daops.ops.subset import subset
from roocs_utils.parameter.param_utils import time_interval
from roocs_utils.parameter.param_utils import time_components
from roocs_utils.parameter.param_utils import level_series


def time_window_arg(val):
    start, end = val.split('/')
    return time_interval(start, end)


def time_components_arg(val):
    d = {}
    for bit in val.split('|'):
        time_type, time_vals_str = val.split(':')
        d[time_type] = time_vals_str
    return time_components(**d)


def levels_arg(val):
    return level_series(val)


def parse_args():

    parser = argparse.ArgumentParser()

    sub_parsers = parser.add_subparsers()

    parser_subset = sub_parsers.add_parser('subset', help='subset data')
    parser_subset.add_argument('--area', '-a', type=str, metavar='area',
                               help=('area in format w,s,e,n. Hint: if w is negative, include an "=" sign '
                                     'e.g. --area=-10,...'))
    parser_subset.add_argument('--time', '-t', type=time_window_arg, metavar='time_window',
                               help='time window e.g. 1999-01-01T00:00:00/2100-12-30T00:00:00')
    parser_subset.add_argument('--time-components', '-c', type=time_components_arg, metavar='time_components',
                               help="time components e.g. month:dec,jan,feb or 'year:1970,1980|month:01,02,03'")
    parser_subset.add_argument('--levels', '-l', type=levels_arg,
                               metavar='levels', help='comma-separated list of levels')
    parser_subset.add_argument('--output-format', '-f', type=str, metavar='format',
                               choices=('netcdf', 'nc', 'zarr'))
    parser_subset.add_argument('--output-dir', '-d', type=str, metavar='output_directory', required=True)
    parser_subset.add_argument('collection', type=str, nargs='+')

    return parser.parse_args()


def get_params(args):
    return {'collection': args.collection,
            'time': args.time,
            'time_components': args.time_components,
            'area': args.area,
            'level': args.levels,
            'output_type': args.output_format,
            'output_dir': args.output_dir,
            'collection': args.collection,
            'apply_fixes': False
            }


def main():
    args = parse_args()
    params = get_params(args)
    ret = subset(**params)
    for uri in ret.file_uris:
        print(uri)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
