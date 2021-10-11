import datetime

from roocs_utils.parameter.time_parameter import TimeParameter

MIN_DATETIME = datetime.datetime(datetime.MINYEAR, 1, 1).isoformat()
MAX_DATETIME = datetime.datetime(datetime.MAXYEAR, 12, 30).isoformat()


def parse_time(time):
    if isinstance(time, TimeParameter):
        time_ = time
    else:
        time_ = TimeParameter(time)
    start, end = time_.get_bounds()

    if not start:
        start = MIN_DATETIME
    if not end:
        end = MAX_DATETIME

    return start, end
