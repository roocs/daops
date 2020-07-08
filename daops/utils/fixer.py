import json
import os

from .core import resolve_import
from elasticsearch import Elasticsearch
from pydoc import locate


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
        self.es = Elasticsearch(
            [f'es{i}.ceda.ac.uk' for i in range(9, 17)],
            use_ssl=True)
        # ca_certs='cert.pem',
        # port=9200)
        self._lookup_fix()

    def _convert_id(self, id):
        m = hashlib.md5()
        m.update(id.encode("utf-8"))
        return m.hexdigest()

    def _lookup_fix(self):
        id = self._convert_id(self.ds_id)
        content = es.get(index='roocs-fix', id=id)
        for fix in content["fixes"]:
            ref_implementation = fix["reference_implementation"]
            func = locate(ref_implementation)

        fix_file = os.path.join(self.FIX_DIR, f'{self.ds_id}.json')

        if not os.path.isfile(fix_file):
            self.pre_processor = None
            self.post_processor = None
            self.pre_processors = ()

        else:
            content = json.load(open(fix_file))
            pre_processors = content.get('pre_processors', None)
            post_processors = content.get('post_processors', None)

            if pre_processors:
                self.pre_processors = []
                for pre_processor in pre_processors:
                    self.pre_processors.append(resolve_import(pre_processor['func']))
            else:
                self.pre_processors = ()
            self.pre_processor = FuncChainer(self.pre_processors)

            if post_processors:
                post_process_list = []
                for post_processor in post_processors:
                    post_process_list.append((resolve_import(post_processor['func']),
                                              post_processor.get('args', None) or [],
                                              post_processor.get('kwargs', None) or {}))
                self.post_processor = post_process_list
            else:
                self.post_processor = ()