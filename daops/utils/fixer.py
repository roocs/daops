import json
import os

from elasticsearch import Elasticsearch, exceptions
from pydoc import locate
import hashlib


class FuncChainer(object):

    def __init__(self, funcs):
        self.funcs = funcs

    def __call__(self, inputs):
        result = inputs
        for f in self.funcs:
            result = f(result)
        return result


class Fixer(object):

    def __init__(self, ds_id):
        self.ds_id = ds_id
        self.es = Elasticsearch([f'es{i}.ceda.ac.uk' for i in range(9, 17)],
                                use_ssl=True,
                                ca_certs=os.path.abspath(
                                    os.path.join(
                                        os.path.dirname(__file__), '../root-ca.pem')
                                ),
                                port=9200)
        self._lookup_fix()

    def _convert_id(self, id):
        m = hashlib.md5()
        m.update(id.encode("utf-8"))
        return m.hexdigest()

    def _gather_fixes(self, content):
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
        id = self._convert_id(self.ds_id)

        self.pre_processor = None
        self.pre_processors = []
        self.post_processors = []

        try:
            content = self.es.get(index='roocs-fix', id=id)
            self._gather_fixes(content)
        except exceptions.NotFoundError:
            pass
