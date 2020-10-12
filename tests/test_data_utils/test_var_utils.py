from daops.data_utils.var_utils import reverse_2d_vars

import xarray as xr
import numpy as np


def test_reverse_2d_vars():
    ds = xr.open_mfdataset(
        "tests/mini-esgf-data/test_data/badc/cmip6/data/CMIP6/CMIP/NCAR/CESM2/amip/r1i1p1f1/Amon/cl/gn/v20190319/*.nc",
        combine="by_coords",
        use_cftime=True,
    )

    assert np.isclose(ds.a_bnds.values[0][0], 0)
    assert np.isclose(ds.a_bnds.values[-1][-1], 0.00225524)

    assert np.isclose(ds.b_bnds.values[0][0], 1)
    assert np.isclose(ds.b_bnds.values[-1][-1], 0)

    operands = {
        "var_ids": ['a_bnds',
                    'b_bnds']
    }

    ds_reverse = reverse_2d_vars(ds, **operands)

    assert np.isclose(ds_reverse.a_bnds.values[0][0], 0.00225524)
    assert np.isclose(ds_reverse.a_bnds.values[-1][-1], 0)
    assert ds_reverse.a_bnds.attrs == ds.a_bnds.attrs

    assert np.isclose(ds_reverse.b_bnds.values[0][0], 0)
    assert np.isclose(ds_reverse.b_bnds.values[-1][-1], 1)
    assert ds_reverse.b_bnds.attrs == ds.b_bnds.attrs
