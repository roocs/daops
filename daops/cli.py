"""Console script for daops."""

__author__ = """Alan Iwi"""
__contact__ = "alan.iwi@stfc.ac.uk"
__copyright__ = "Copyright 2023 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import os
import sys
import argparse
import dateutil.parser
import configparser

from daops.ops.subset import subset
from roocs_utils.utils.file_utils import FileMapper


def parse_args():
    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers()
    sub_parsers.required = True

    parser_subset = sub_parsers.add_parser("subset", help="subset data")
    parser_subset.add_argument(
        "--area",
        "-a",
        type=str,
        help=(
            'area in format w,s,e,n. Hint: if w is negative, include an "=" sign '
            "e.g. --area=-10,..."
        ),
    )
    parser_subset.add_argument(
        "--time",
        "-t",
        type=str,
        metavar="time_window",
        help="time window e.g. 1999-01-01T00:00:00/2100-12-30T00:00:00",
    )
    parser_subset.add_argument(
        "--time-components",
        "-c",
        type=str,
        help="time components e.g. month:dec,jan,feb or 'year:1970,1980|month:01,02,03'",
    )
    parser_subset.add_argument(
        "--levels",
        "-l",
        type=str,
        help=(
            "comma-separated list of levels (e.g. 500,1000,2000) "
            "or slash-separated range (e.g. 50/2000 for 50 to 2000)"
        ),
    )
    parser_subset.add_argument(
        "--output-format",
        "-f",
        type=str,
        metavar="format",
        choices=("netcdf", "nc", "zarr"),
        default="netcdf",
    )
    parser_subset.add_argument(
        "--file-namer",
        "-F",
        type=str,
        choices=("simple", "standard"),
        default="standard",
    )
    parser_subset.add_argument(
        "--output-dir", "-d", type=str, metavar="output_directory", required=True
    )
    parser_subset.add_argument("collection", type=str, nargs="+", default=list)

    return parser.parse_args()


def get_params(args):
    collection = (
        args.collection if len(args.collection) == 1 else FileMapper(args.collection)
    )

    return {
        "collection": collection,
        "time": args.time,
        "time_components": args.time_components,
        "area": args.area,
        "level": args.levels,
        "output_type": args.output_format,
        "output_dir": args.output_dir,
        "file_namer": args.file_namer,
        "apply_fixes": False,
    }


def check_env():
    """
    Check that ROOCS_CONFIG points to a valid config file
    (although for certain types of invalid file, in fact main is never called,
    so exit might not always be graceful in these cases).
    Call this after get_params() so that 'help' still works even if this is not set.
    """
    config_env_var = "ROOCS_CONFIG"
    c = configparser.ConfigParser()
    try:
        ret = c.read(os.environ[config_env_var])
    except (KeyError, configparser.Error):
        ret = None
    if not ret:
        print(
            f"Environment variable {config_env_var} must contain the path name of a config file in ini format"
        )
        sys.exit(1)


def main():
    args = parse_args()
    params = get_params(args)
    check_env()
    ret = subset(**params)
    for uri in ret.file_uris:
        print(uri)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
