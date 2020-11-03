from daops.utils.consolidate import _consolidate_dset
from tests._common import TESTS_HOME


def test_consolidate_dset():
    dset = "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"
    consolidated = _consolidate_dset(dset)
    assert (
        consolidated
        == f"{TESTS_HOME}/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/"
        f"INM/inmcm4/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*.nc"
    )

    dset = "/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc"
    consolidated = _consolidate_dset(dset)
    assert consolidated == dset

    dset = (
        "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos"
        "/Amon/r1i1p1/latest/tas/"
    )
    consolidated = _consolidate_dset(dset)
    assert consolidated == dset + "*.nc"
