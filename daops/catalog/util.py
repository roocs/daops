import datetime

from roocs_utils.parameter import time_parameter

MIN_DATETIME = datetime.datetime(datetime.MINYEAR, 1, 1).isoformat()
MAX_DATETIME = datetime.datetime(datetime.MAXYEAR, 12, 30).isoformat()


def parse_time(time):
    # TODO: refactor code ... maybe we need this only in the catalog. allow dicts in time parameter?
    if isinstance(time, dict):
        time = (time["start_time"], time["end_time"])
    start, end = time_parameter.TimeParameter(time).tuple

    if not start:
        start = MIN_DATETIME
    if not end:
        end = MAX_DATETIME

    return start, end
