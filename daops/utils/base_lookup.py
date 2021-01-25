import hashlib
import os

from elasticsearch import Elasticsearch
from roocs_utils.exceptions import InvalidProject
from roocs_utils.project_utils import derive_ds_id

from daops import CONFIG


class Lookup(object):
    """
    Base class used for looking up datasets in the elasticsearch indexes.
    """

    def __init__(self, dset):
        self.dset = dset
        self.es = Elasticsearch(
            [CONFIG["elasticsearch"]["endpoint"]],
            use_ssl=True,
            port=CONFIG["elasticsearch"]["port"],
        )

    def convert_to_ds_id(self):
        """ Converts the input dataset to a drs id form to use with the elasticsearch index. """
        try:
            return derive_ds_id(self.dset)
        # projects = [_.split(":")[1] for _ in CONFIG.keys() if _.startswith("project:")]
        # if self.dset.startswith("https"):
        #     raise Exception("This format is not supported yet")
        # elif os.path.isfile(self.dset) or self.dset.endswith(".nc"):
        #     dset = self.dset.split("/")
        #     i = max(loc for loc, val in enumerate(dset) if val.lower() in projects)
        #     ds_id = ".".join(dset[i:-1])
        #     return ds_id
        # elif os.path.isdir(self.dset):
        #     dset = self.dset.split("/")
        #     i = max(loc for loc, val in enumerate(dset) if val.lower() in projects)
        #     ds_id = ".".join(dset[i:])
        #     return ds_id
        except InvalidProject:
            raise Exception(
                f"The format of {self.dset} is not known and it could not be converted to a ds id."
            )

    def _convert_id(self, _id):
        """
        Converts the dataset id to an md5 checksum used to retrieve the fixes for the dataset. Converts to drs id
        format first if necessary.
        """
        if _id.count(".") < 6:
            _id = self.convert_to_ds_id()

        m = hashlib.md5()
        m.update(_id.encode("utf-8"))
        return m.hexdigest()
