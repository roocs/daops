"""Base class used for looking up datasets in the elasticsearch indexes."""

import hashlib

from clisops.exceptions import InvalidProject
from clisops.project_utils import derive_ds_id
from elasticsearch import Elasticsearch

from daops import config_


class Lookup:
    """Base class used for looking up datasets in the elasticsearch indexes."""

    def __init__(self, dset):  # noqa: D107
        self.dset = dset
        self.es = Elasticsearch(
            "https://"
            + config_()["elasticsearch"]["endpoint"]
            + ":"
            + config_()["elasticsearch"]["port"],
        )

    def convert_to_ds_id(self):
        """Convert the input dataset to a drs id form to use with the elasticsearch index."""
        try:
            return derive_ds_id(self.dset)
        except InvalidProject as err:
            raise Exception(
                f"The format of {self.dset} is not known and it could not be converted to a ds id."
            ) from err

    def _convert_id(self, _id):
        """Convert the dataset id to an md5 checksum used to retrieve the fixes for the dataset.

        Converts to drs id format first if necessary.
        """
        _id = self.convert_to_ds_id()

        m = hashlib.md5()  # noqa: S324
        m.update(_id.encode("utf-8"))
        return m.hexdigest()
