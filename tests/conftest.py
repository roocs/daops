from clisops.utils.testing import stratus as _stratus

from clisops.utils.testing import (
    ESGF_TEST_DATA_CACHE_DIR,
    ESGF_TEST_DATA_REPO_URL,
    ESGF_TEST_DATA_VERSION,
    gather_testing_data,
)

import pytest

from daops.utils.testing import write_roocs_cfg as _write_roocs_cfg, get_esgf_file_paths


@pytest.fixture
def cmip6_kerchunk_https_open_json():
    return (
        "https://gws-access.jasmin.ac.uk/public/cmip6_prep/eodh-eocis/kc-indexes-cmip6-http-v1/"
        "CMIP6.CMIP.MOHC.UKESM1-1-LL.1pctCO2.r1i1p1f2.Amon.tasmax.gn.v20220513.json"
    )


@pytest.fixture(scope="session", autouse=True)
def write_roocs_cfg(stratus):
    _write_roocs_cfg(stratus.path)
    # TODO: reload configs in clisops
    # workaround ... fix code in new clisops.
    import daops
    import clisops

    cfg = daops.config_()
    clisops.CONFIG = cfg
    # clisops.core.regrid.CONFIG = cfg
    # clisops.utils.file_namers.CONFIG = cfg
    # clisops.utils.output_utils.CONFIG = cfg
    clisops.project_utils.CONFIG = cfg
    # print("clisops.config", clisops.CONFIG["project:cmip5"]["base_dir"])


@pytest.fixture
def tmp_netcdf_filename(tmp_path):
    return tmp_path.joinpath("testfile.nc")


@pytest.fixture(scope="session")
def stratus():
    return _stratus(
        repo=ESGF_TEST_DATA_REPO_URL,
        branch=ESGF_TEST_DATA_VERSION,
        cache_dir=(ESGF_TEST_DATA_CACHE_DIR),
    )


@pytest.fixture(scope="session", autouse=True)
def load_test_data(stratus):
    """
    This fixture ensures that the required test data repository
    has been cloned to the cache directory within the home directory.
    """
    repositories = {
        "stratus": {
            "worker_cache_dir": stratus.path,
            "repo": ESGF_TEST_DATA_REPO_URL,
            "branch": ESGF_TEST_DATA_VERSION,
            "cache_dir": ESGF_TEST_DATA_CACHE_DIR,
        },
    }

    for name, repo in repositories.items():
        gather_testing_data(worker_id="master", **repo)


@pytest.fixture(scope="session", autouse=True)
def mini_esgf_data(stratus):
    return get_esgf_file_paths(stratus.path)
