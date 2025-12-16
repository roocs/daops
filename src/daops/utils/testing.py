import os
from pathlib import Path
from typing import Optional

from _pytest.logging import LogCaptureFixture
from clisops.utils.testing import ESGF_TEST_DATA_CACHE_DIR, ESGF_TEST_DATA_VERSION
from jinja2 import Template


def write_roocs_cfg(cache_dir: str | Path):
    cfg_templ = """
    [project:cmip5]
    base_dir = {{ base_dir }}/badc/cmip5/data/cmip5

    [project:cmip6]
    base_dir = {{ base_dir }}/badc/cmip6/data/CMIP6

    [project:cordex]
    base_dir = {{ base_dir }}/badc/cordex/data/cordex

    [project:c3s-cmip5]
    base_dir = {{ base_dir }}/gws/nopw/j04/cp4cds1_vol1/data/c3s-cmip5

    [project:c3s-cmip6]
    base_dir = {{ base_dir }}/badc/cmip6/data/CMIP6

    [project:c3s-cordex]
    base_dir = {{ base_dir }}/gws/nopw/j04/cp4cds1_vol1/data/c3s-cordex
    """
    roocs_config = Path(cache_dir, "roocs.ini")
    cfg = Template(cfg_templ).render(
        base_dir=Path(ESGF_TEST_DATA_CACHE_DIR).joinpath(ESGF_TEST_DATA_VERSION)
    )
    with open(roocs_config, "w") as fp:
        fp.write(cfg)

    # point to roocs cfg in environment
    os.environ["ROOCS_CONFIG"] = roocs_config.as_posix()


def get_esgf_file_paths(esgf_cache_dir: str | os.PathLike[str]):
    return {
        "CMIP5_TAS_FPATH": Path(
            esgf_cache_dir,
            "badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_200512-203011.nc",
        ).as_posix(),
        "CMIP5_DAY": Path(
            esgf_cache_dir,
            "badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/land/day/r1i1p1/latest/mrsos/mrsos_day_HadGEM2-ES_rcp45_r1i1p1_20051201-20151130.nc",
        ).as_posix(),
        "CMIP6_MONTH": Path(
            esgf_cache_dir,
            "badc/cmip6/data/CMIP6/CMIP/CCCma/CanESM5/historical/r1i1p1f1/SImon/siconc/gn/latest/siconc_SImon_CanESM5_historical_r1i1p1f1_gn_185001-201412.nc",
        ).as_posix(),
        "CMIP6_DAY": Path(
            esgf_cache_dir,
            "badc/cmip6/data/CMIP6/CMIP/CCCma/CanESM5/historical/r1i1p1f1/SIday/siconc/gn/v20190429/siconc_SIday_CanESM5_historical_r1i1p1f1_gn_18500101-20141231.nc",
        ).as_posix(),
        "CMIP6_DECADAL": Path(
            esgf_cache_dir,
            "badc/cmip6/data/CMIP6/DCPP/MOHC/HadGEM3-GC31-MM/dcppA-hindcast/s2004-r3i1p1f2/Amon/pr/gn/v20200417/pr_Amon_HadGEM3-GC31-MM_dcppA-hindcast_s2004-r3i1p1f2_gn_200411-200412.nc",
        ).as_posix(),
    }


class ContextLogger:
    """Helper function for safe logging management in pytests."""

    def __init__(self, caplog: Optional[LogCaptureFixture] = None):  # noqa: UP045
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
