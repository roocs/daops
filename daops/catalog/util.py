import datetime

from roocs_utils.parameter import time_parameter

MIN_DATETIME = datetime.datetime(datetime.MINYEAR, 1, 1).isoformat()
MAX_DATETIME = datetime.datetime(datetime.MAXYEAR, 12, 30).isoformat()


def parse_time(time):
    # TODO: refactor code ... maybe we need this only in the catalog.
    if time:
        start, end = time_parameter.TimeParameter(time).tuple
    else:
        start = MIN_DATETIME
        end = MAX_DATETIME
    return start, end
