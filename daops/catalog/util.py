import datetime

from roocs_utils.parameter.time_parameter import TimeParameter, time_interval

MIN_DATETIME = datetime.datetime(datetime.MINYEAR, 1, 1).isoformat()
MAX_DATETIME = datetime.datetime(datetime.MAXYEAR, 12, 30).isoformat()


def parse_time(time):
    
    if isinstance(time, TimeParameter):
        start, end = time.get_bounds()
    elif time is None or set(time) == {None}:
        start, end = None, None
    else:
        start, end = TimeParameter(time_interval(time)).value

    if not start:
        start = MIN_DATETIME
    if not end:
        end = MAX_DATETIME

    return start, end
