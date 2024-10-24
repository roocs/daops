from daops.utils.base_lookup import Lookup

from tests._common import MINI_ESGF_MASTER_DIR


def test_convert_to_ds_id(load_esgf_test_data):
    fpath = (
        f"{MINI_ESGF_MASTER_DIR}/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES"
        f"/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc"
    )
    ds_id = Lookup(fpath).convert_to_ds_id()
    assert (
        ds_id == "cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas"
    )
