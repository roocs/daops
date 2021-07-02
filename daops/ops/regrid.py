from clisops.ops.regrid import regrid as clisops_regrid
from roocs_utils.parameter import collection_parameter
from roocs_utils.parameter import dimension_parameter

from daops.ops.base import Operation

__all__ = [
    "regrid",
]


class Regrid(Operation):
    def _resolve_params(self, collection, **params):
        """
        Resolve the input parameters to `self.params` and parameterise
        collection parameter and set to `self.collection`.
        """
        # need to verify method, grid and adaptive masking threshold are correct format - parameters?
        collection = collection_parameter.CollectionParameter(collection)

        self.collection = collection
        self.params = {
            "method": params.get("method"),
            "adaptive_masking_threshold": params.get("adaptive_masking_threshold"),
            "grid": params.get("grid"),
        }

    def get_operation_callable(self):
        return clisops_regrid


def regrid(
    collection,
    method="nn",
    adaptive_masking_threshold=0.5,
    grid="1deg",
    output_dir=None,
    output_type="netcdf",
    split_method="time:auto",
    file_namer="standard",
    apply_fixes=True,
):
    """
    Regrid input dataset according to specified method and output grid.
    The adaptive masking threshold can also be specified.

    Parameters
    ----------
    collection: Collection of datasets to process, sequence or string of comma separated dataset identifiers.
    method: The method by which to regrid.
    adaptive_masking_threshold:
    grid: The desired output grid.
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
    | method: "nn"
    | adaptive_masking_threshold: 0.5
    | grid: "1deg"
    | output_type: "netcdf"
    | output_dir: "/cache/wps/procs/req0111"
    | split_method: "time:auto"
    | file_namer: "standard"
    | apply_fixes: True

    """

    result_set = Regrid(**locals()).calculate()

    return result_set
