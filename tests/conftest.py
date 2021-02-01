import os
import shutil

import numpy as np
import pandas as pd
import pytest
import xarray as xr

from tests._common import MINI_ESGF_CACHE_DIR, write_roocs_cfg, MINI_ESGF_MASTER_DIR

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
    tmp_repo = "/tmp/.mini-esgf-data"
    test_data_dir = os.path.join(tmp_repo, "test_data")

    if not os.path.isdir(MINI_ESGF_MASTER_DIR):

        os.makedirs(MINI_ESGF_MASTER_DIR)
        os.system(f"git clone {ESGF_TEST_DATA_REPO_URL} {tmp_repo}")

        shutil.move(test_data_dir, MINI_ESGF_MASTER_DIR)
        shutil.rmtree(tmp_repo)
