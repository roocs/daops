from daops.utils.base_lookup import Lookup


def test_convert_to_ds_id(stratus):
    fpath = (
        f"{stratus.path}/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES"
        f"/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc"
    )
    ds_id = Lookup(fpath).convert_to_ds_id()
    assert (
        ds_id == "cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas"
    )
