from clisops.ops.subset import subset as clisops_subset
from roocs_utils.parameter import parameterise

from daops.ops.base import Operation

__all__ = [
    "subset",
]


class Subset(Operation):
    def _resolve_params(self, collection, **params):
        """
        Resolve the subset parameters to `self.params` and parameterise
        collection parameter and set to self.collection.
        """
        parameters = parameterise(
            collection=collection,
            time=params.get("time"),
            area=params.get("area"),
            level=params.get("level"),
        )

        self.collection = parameters.pop("collection")
        self.params = parameters

    def get_operation_callable(self):
        return clisops_subset


def subset(
    collection,
    time=None,
    area=None,
    level=None,
    output_dir=None,
    output_type="netcdf",
    split_method="time:auto",
    file_namer="standard",
    apply_fixes=True,
):
    """
    Subset input dataset according to parameters.
    Can be subsetted by level, area and time.

    Parameters
    ----------
    collection: Collection of datasets to process, sequence or string of comma separated dataset identifiers.
    time: Time period - Time range to subset over, sequence of two time values or string of two / separated time values
    area: Area to subset over, sequence or string of comma separated lat and lon bounds. Must contain 4 values.
    level: Level range - Level values to subset over, sequence of two level values or string of two / separated level values
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
    | time: ("1999-01-01T00:00:00", "2100-12-30T00:00:00")
    | area: (-5.,49.,10.,65)
    | level: (1000.,)
    | output_type: "netcdf"
    | output_dir: "/cache/wps/procs/req0111"
    | split_method: "time:auto"
    | file_namer: "standard"
    | apply_fixes: True

    """

    result_set = Subset(**locals()).calculate()

    return result_set
