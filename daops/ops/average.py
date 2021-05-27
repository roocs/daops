from clisops.ops.average import average_over_dims as clisops_average_over_dims
from roocs_utils.parameter import collection_parameter
from roocs_utils.parameter import dimension_parameter

from daops.ops.base import Operation

__all__ = [
    "average_over_dims",
]


class Average(Operation):
    def _resolve_params(self, collection, **params):
        """
        Resolve the input parameters to `self.params` and parameterise
        collection parameter and set to `self.collection`.
        """
        dims = dimension_parameter.DimensionParameter(params.get("dims"))
        collection = collection_parameter.CollectionParameter(collection)

        self.collection = collection
        self.params = {
            "dims": dims,
            "ignore_undetected_dims": params.get("ignore_undetected_dims"),
        }

    def get_operation_callable(self):
        return clisops_average_over_dims


def average_over_dims(
    collection,
    dims=None,
    ignore_undetected_dims=False,
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
    ignore_undetected_dims: Boolean. If False exception will be raised if requested dims do not exist in the dataset
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
    | dims: ["time", "lat"]
    | ignore_undetected_dims: (-5.,49.,10.,65)
    | output_type: "netcdf"
    | output_dir: "/cache/wps/procs/req0111"
    | split_method: "time:auto"
    | file_namer: "standard"
    | apply_fixes: True

    """

    result_set = Average(**locals()).calculate()

    return result_set
