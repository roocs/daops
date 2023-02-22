"""Console script for daops."""

__author__ = """Alan Iwi"""
__contact__ = 'alan.iwi@stfc.ac.uk'
__copyright__ = "Copyright 2023 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


import argparse
import sys
import dateutil.parser

from daops.ops.subset import subset


def area_arg(val):
    bits = val.split(',')
    if len(bits) != 4:
        raise ValueError
    return [float(bit) for bit in bits]


def time_window_arg(val):
    bits = val.split(',')
    if len(bits) != 2:
        raise ValueError
    return [dateutil.parser.parse(bit) for bit in bits]


def time_component(val):
    time_type, time_vals_str = val.split(':')
    bits = time_vals_str.split(',')
    if time_type in ('year', 'day', 'hour', 'minute', 'second'):
        time_vals = [int(bit) for bit in bits]
    elif time_type == 'month':
        time_vals = []
        for bit in bits:
            try:
                time_vals.append(int(bit))
            except ValueError:
                time_vals.append(bit)
    else:
        raise ValueError
    return time_type, time_vals


def time_components_arg(val):
    d = {}
    for bit in val.split('|'):
        k, v = time_component(bit)
        d[k] = v
    return d


def levels_arg(val):
    return [float(bit) for bit in val.split(',')]


def parse_args():

    parser = argparse.ArgumentParser()

    sub_parsers = parser.add_subparsers()

    parser_subset = sub_parsers.add_parser('subset', help='subset data')
    parser_subset.add_argument('--area', '-a', type=area_arg, metavar='w,s,e,n')
    parser_subset.add_argument('--time', '-t', type=time_window_arg, metavar='time_window',
                               help='time window e.g. 1999-01-01T00:00:00,2100-12-30T00:00:00')
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
            'output_type': args.output_format,
            'output_dir': args.output_dir,
            'collection': args.collection,
            'apply_fixes': False
            }


def main():
    args = parse_args()
    params = get_params(args)
    print(params)
    ret = subset(**params)
    print(ret.file_uris)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
