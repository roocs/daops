import os
import tempfile
from pathlib import Path
from typing import Optional

from _pytest.logging import LogCaptureFixture
from jinja2 import Template

TESTS_HOME = os.path.abspath(os.path.dirname(__file__))
TESTS_OUTPUTS = os.path.join(TESTS_HOME, "_outputs")
ROOCS_CFG = os.path.join(tempfile.gettempdir(), "roocs.ini")

MINI_ESGF_CACHE_DIR = Path.home() / ".mini-esgf-data"
MINI_ESGF_MASTER_DIR = os.path.join(MINI_ESGF_CACHE_DIR, "master")

try:
    os.mkdir(TESTS_OUTPUTS)
except Exception:
    pass


class ContextLogger:
    """Helper function for safe logging management in pytests"""

    def __init__(self, caplog: Optional[LogCaptureFixture] = False):
        from loguru import logger

        self.logger = logger
        self.using_caplog = False
        if caplog:
            self.using_caplog = True

    def __enter__(self):
        self.logger.enable("daops")
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        """If test is supplying caplog, pytest will manage teardown."""

        self.logger.disable("daops")
        if not self.using_caplog:
            try:
                self.logger.remove()
            except ValueError:
                pass


def write_roocs_cfg():
    cfg_templ = """
    [project:cmip5]
    base_dir = {{ base_dir }}/test_data/badc/cmip5/data/cmip5

    [project:cmip6]
    base_dir = {{ base_dir }}/test_data/badc/cmip6/data/CMIP6

    [project:cordex]
    base_dir = {{ base_dir }}/test_data/badc/cordex/data/cordex

    [project:c3s-cmip5]
    base_dir = {{ base_dir }}/test_data/gws/nopw/j04/cp4cds1_vol1/data/c3s-cmip5

    [project:c3s-cmip6]
    base_dir = {{ base_dir }}/test_data/badc/cmip6/data/CMIP6

    [project:c3s-cordex]
    base_dir = {{ base_dir }}/test_data/gws/nopw/j04/cp4cds1_vol1/data/c3s-cordex
    """
    cfg = Template(cfg_templ).render(base_dir=MINI_ESGF_MASTER_DIR)
    with open(ROOCS_CFG, "w") as fp:
        fp.write(cfg)

    # point to roocs cfg in environment
    os.environ["ROOCS_CONFIG"] = ROOCS_CFG


CMIP5_TAS_FPATH = Path(
    MINI_ESGF_MASTER_DIR,
    "test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_200512-203011.nc",
).as_posix()

CMIP5_DAY = Path(
    MINI_ESGF_MASTER_DIR,
    "test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/land/day/r1i1p1/latest/mrsos/mrsos_day_HadGEM2-ES_rcp45_r1i1p1_20051201-20151130.nc",
).as_posix()

CMIP6_MONTH = Path(
    MINI_ESGF_MASTER_DIR,
    "test_data/badc/cmip6/data/CMIP6/CMIP/CCCma/CanESM5/historical/r1i1p1f1/SImon/siconc/gn/latest/siconc_SImon_CanESM5_historical_r1i1p1f1_gn_185001-201412.nc",
).as_posix()

CMIP6_DAY = Path(
    MINI_ESGF_MASTER_DIR,
    "test_data/badc/cmip6/data/CMIP6/CMIP/CCCma/CanESM5/historical/r1i1p1f1/SIday/siconc/gn/v20190429/siconc_SIday_CanESM5_historical_r1i1p1f1_gn_18500101-20141231.nc",
).as_posix()

CMIP6_DECADAL = Path(
    MINI_ESGF_MASTER_DIR,
    "test_data/badc/cmip6/data/CMIP6/DCPP/MOHC/HadGEM3-GC31-MM/dcppA-hindcast/s2004-r3i1p1f2/Amon/pr/gn/v20200417/pr_Amon_HadGEM3-GC31-MM_dcppA-hindcast_s2004-r3i1p1f2_gn_200411-200412.nc",
).as_posix()

CMIP6_KERCHUNK_HTTPS_OPEN_JSON = ("https://gws-access.jasmin.ac.uk/public/cmip6_prep/eodh-eocis/kc-indexes-cmip6-http-v1/"
                                  "CMIP6.CMIP.MOHC.UKESM1-1-LL.1pctCO2.r1i1p1f2.Amon.tasmax.gn.v20220513.json")
