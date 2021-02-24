import os
import shutil

from git import Repo
import numpy as np
import pandas as pd
import pytest
import xarray as xr

from tests._common import MINI_ESGF_CACHE_DIR, write_roocs_cfg

write_roocs_cfg()

ESGF_TEST_DATA_REPO_URL = "https://github.com/roocs/mini-esgf-data"


@pytest.fixture
def tmp_netcdf_filename(tmp_path):
    return tmp_path.joinpath("testfile.nc")


# Fixture to load mini-esgf-data repository used by roocs tests
@pytest.fixture
def load_esgf_test_data():
    """
    This fixture ensures that the required test data repository
    has been cloned to the cache directory within the home directory.
    """
    branch = "master"
    target = os.path.join(MINI_ESGF_CACHE_DIR, branch)

    if not os.path.isdir(MINI_ESGF_CACHE_DIR):
        os.makedirs(MINI_ESGF_CACHE_DIR)

    if not os.path.isdir(target):
        repo = Repo.clone_from(ESGF_TEST_DATA_REPO_URL, target)
        repo.git.checkout(branch)

    elif os.environ.get("ROOCS_AUTO_UPDATE_TEST_DATA", "true").lower() != "false":
        repo = Repo(target)
        repo.git.checkout(branch)
        repo.remotes[0].pull()
