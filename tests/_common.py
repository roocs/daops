import os
from unittest import mock
import pytest


TESTS_HOME = os.path.abspath(os.path.dirname(__file__))
TESTS_OUTPUTS = os.path.join(TESTS_HOME, "_outputs")

try:
    # TODO: better use tempfile.mkstemp()?
    os.mkdir(TESTS_OUTPUTS)
except Exception:
    pass


tests_project_base_dirs = {
    "cmip5": "tests/mini-esgf-data/test_data/badc/cmip5/data",
    "cmip6": "tests/mini-esgf-data/test_data/badc/cmip6/data",
    "cordex": "tests/mini-esgf-data/test_data/badc/cordex/data",
    "c3s-cmip5": "tests/mini-esgf-data/test_data/group_workspaces/jasmin2/cp4cds1/vol1/data/",
    "c3s-cmip6": "NOT DEFINED YET",
    "c3s-cordex": "tests/mini-esgf-data/test_data/group_workspaces/jasmin2/cp4cds1/vol1/data/",
}


def get_tests_project_base_dir(project):
    return tests_project_base_dirs.get(project)
