from roocs_utils.parameter import collection_parameter

from daops.processor import process
from daops.utils import consolidate
from daops.utils import normalise


class Operation:
    """
    Base class for all Operations.
    """

    def __init__(
        self,
        collection,
        file_namer="standard",
        split_method="time:auto",
        output_dir=None,
        output_type="netcdf",
        apply_fixes=True,
        **params,
    ):
        """
        Constructor for each operation.
        Sets common input parameters as attributes.
        Parameters that are specific to each operation are handled in:
          self._resolve_params()
        """
        self._file_namer = file_namer
        self._split_method = split_method
        self._output_dir = output_dir
        self._output_type = output_type
        self._apply_fixes = apply_fixes
        self._resolve_params(collection, **params)
        self._consolidate_collection()

    def _resolve_params(self, collection, **params):
        """
        Resolve the operation-specific input parameters to `self.params` and parameterise
        collection parameter and set to `self.collection`.
        """
        self.collection = collection_parameter.CollectionParameter(collection)
        self.params = params

    def _consolidate_collection(self):
        """
        Take in the collection object and finds the file paths relating to each input dataset.
        If a time range has been supplied then then only the files relating to this time range are recorded.
        Set the result to `self.collection`.
        """

        if "time" in self.params:
            self.collection = consolidate.consolidate(
                self.collection, time=self.params.get("time")
            )

        else:
            self.collection = consolidate.consolidate(self.collection)

    def get_operation_callable(self):
        raise NotImplementedError

    def calculate(self):
        """
        The `calculate()` method processes the input and calculates the result using clisops.
        It then returns the result as a daops.normalise.ResultSet object
        """
        config = {
            "output_type": self._output_type,
            "output_dir": self._output_dir,
            "split_method": self._split_method,
            "file_namer": self._file_namer,
        }

        self.params.update(config)

        # Normalise (i.e. "fix") data inputs based on "character"
        norm_collection = normalise.normalise(self.collection, self._apply_fixes)

        rs = normalise.ResultSet(vars())

        # change name of data ref here
        for dset, norm_collection in norm_collection.items():
            # Process each input dataset (either in series or
            # parallel)
            rs.add(
                dset,
                process(self.get_operation_callable(), norm_collection, **self.params),
            )

        return rs
