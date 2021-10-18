from daops.catalog.util import parse_time


def test_parse_time():
    # only time
    assert parse_time(time="2001/2010") == (
        "2001-01-01T00:00:00",
        "2010-12-31T23:59:59",
    )
    # only time components
    assert parse_time(time_components="year:2005,2006") == (
        "2005-01-01T00:00:00",
        "2006-12-31T23:59:59",
    )
    # both ... time wins
    assert parse_time(time="2001/2010", time_components="year:2005,2006") == (
        "2001-01-01T00:00:00",
        "2010-12-31T23:59:59",
    )
