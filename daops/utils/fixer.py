import json
import os

from elasticsearch import Elasticsearch, exceptions
from ceda_elasticsearch_tools.elasticsearch import CEDAElasticsearchClient
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


# class Fixer(object):
#
#     FIX_DIR = './fixes'
#
#     def __init__(self, ds_id):
#         self.ds_id = ds_id
#         self._lookup_fix()
#
#     def _lookup_fix(self):
#         fix_file = os.path.join(self.FIX_DIR, f'{self.ds_id}.json')
#
#         if not os.path.isfile(fix_file):
#             self.pre_processor = None
#             self.post_processor = None
#             self.pre_processors = ()
#
#         else:
#             content = json.load(open(fix_file))
#             pre_processors = content.get('pre_processors', None)
#             post_processors = content.get('post_processors', None)
#
#             if pre_processors:
#                 self.pre_processors = []
#                 for pre_processor in pre_processors:
#                     self.pre_processors.append(resolve_import(pre_processor['func']))
#             else:
#                 self.pre_processors = ()
#             self.pre_processor = FuncChainer(self.pre_processors)
#
#             if post_processors:
#                 post_process_list = []
#                 for post_processor in post_processors:
#                     post_process_list.append((resolve_import(post_processor['func']),
#                                               post_processor.get('args', None) or [],
#                                               post_processor.get('kwargs', None) or {}))
#                 self.post_processor = post_process_list
#             else:
#                 self.post_processor = ()


class Fixer(object):

    def __init__(self, ds_id):
        self.ds_id = ds_id
        self.es = CEDAElasticsearchClient()
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
