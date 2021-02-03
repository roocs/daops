import xarray as xr
from clisops.ops.average import average_over_dims as clisops_average_over_dims
from roocs_utils.parameter import parameterise

from daops.processor import process
from daops.utils import consolidate
from daops.utils import normalise

__all__ = [
    "average_over_dims",
]


def average_over_dims(
    collection,
    dims,
    ignore_unfound_dims=False,
    output_dir=None,
    output_type="netcdf",
    split_method="time:auto",
    file_namer="standard",
    apply_fixes=True,
):
    """
    Average input dataset according over indicated dimensions.
    Can be averaged over multiple dimensions.

    Parameters
    ----------
    collection: Collection of datasets to process, sequence or string of comma separated dataset identifiers.
    dims: list of dims to average over or None.
    ignore_unfound_dims: Boolean. If False exception will be raised if requested dims do not exist in the dataset
    If True missing dims will be ignored.
    output_dir: str or path like object describing output directory for output files.
    output_type: {"netcdf", "nc", "zarr", "xarray"}
    split_method: {"time:auto"}
    file_namer: {"standard", "simple"}
    apply_fixes: Boolean. If True fixes will be applied to datasets if needed. Default is True.

    Returns
    -------
    List of outputs in the selected type: a list of xarray Datasets or file paths.


    Examples
    --------
    | collection: ("cmip6.ukesm1.r1.gn.tasmax.v20200101",)
    | dims:
    | ignore_unfound_dims: (-5.,49.,10.,65)
    | output_type: "netcdf"
    | output_dir: "/cache/wps/procs/req0111"
    | split_method: "time:decade"
    | file_namer: "facet_namer"
    | apply_fixes: True

    """

    parameters = parameterise(collection=collection)

    # Consolidate data inputs so they can be passed to Xarray
    collection = consolidate.consolidate(parameters.get("collection"))

    # Normalise (i.e. "fix") data inputs based on "character"
    norm_collection = normalise.normalise(collection, apply_fixes)

    rs = normalise.ResultSet(vars())
    # change name of data ref here
    for dset, norm_collection in norm_collection.items():

        # Process each input dataset (either in series or
        # parallel)
        rs.add(
            dset,
            process(
                clisops_average_over_dims,
                norm_collection,
                **{
                    "dims": dims,
                    "ignore_unfound_dims": ignore_unfound_dims,
                    "output_type": output_type,
                    "output_dir": output_dir,
                    "split_method": split_method,
                    "file_namer": file_namer,
                },
            ),
        )

    return rs
