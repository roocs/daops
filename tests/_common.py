import os

TESTS_HOME = os.path.abspath(os.path.dirname(__file__))
TESTS_OUTPUTS = os.path.join(TESTS_HOME, "_outputs")
DEFAULT_CMIP5_ARCHIVE_BASE = "/badc/cmip5/data/"

try:
    # TODO: better use tempfile.mkstemp()?
    os.mkdir(TESTS_OUTPUTS)
except Exception:
    pass


def cmip5_archive_base():
    if 'CMIP5_ARCHIVE_BASE' in os.environ:
        return os.environ['CMIP5_ARCHIVE_BASE']
    return DEFAULT_CMIP5_ARCHIVE_BASE


CMIP5_ARCHIVE_BASE = cmip5_archive_base()
