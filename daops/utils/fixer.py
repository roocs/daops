import hashlib
import json
import os
from pydoc import locate

from elasticsearch import Elasticsearch
from elasticsearch import exceptions


class FuncChainer(object):
    """ Chains functions together to allow them to be executed in one call."""

    def __init__(self, funcs):
        self.funcs = funcs

    def __call__(self, inputs):
        result = inputs
        for f in self.funcs:
            result = f(result)
        return result


class Fixer(object):
    """
    Fixer class to look up fixes to apply to input dataset from the elastic search index.
    Gathers fixes into pre and post processors.
    Pre-process fixes are chained together to allow them to be executed with one call.
    """

    def __init__(self, ds_id):
        self.ds_id = ds_id
        self.es = Elasticsearch(["elasticsearch.ceda.ac.uk"], use_ssl=True, port=443)
        self._lookup_fix()

    @staticmethod
    def _convert_id(_id):
        """ Converts the dataset id to an md5 checksum used to retrieve the fixes for the dataset."""
        m = hashlib.md5()
        m.update(_id.encode("utf-8"))
        return m.hexdigest()

    def _gather_fixes(self, content):
        """ Gathers pre and post processing fixes together"""
        if content["_source"]["fixes"]:
            for fix in content["_source"]["fixes"]:

                ref_implementation = fix["reference_implementation"]
                func = locate(ref_implementation)

                if fix["process_type"] == "post_processor":
                    self.post_processors.append([func, fix["operands"]])
                else:
                    self.pre_processors.append(func)

            self.pre_processor = FuncChainer(self.pre_processors)

    def _lookup_fix(self):
        """ Looks up fixes on the elasticsearch index."""
        id = self._convert_id(self.ds_id)

        self.pre_processor = None
        self.pre_processors = []
        self.post_processors = []

        try:
            content = self.es.get(index="roocs-fix", id=id)
            self._gather_fixes(content)
        except exceptions.NotFoundError:
            pass
