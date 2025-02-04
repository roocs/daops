"""Apply fixes to input dataset from the elastic search index."""

from pydoc import locate

from elasticsearch import exceptions

from daops import config_

from .base_lookup import Lookup


class FuncChainer:
    """Chains functions together to allow them to be executed in one call."""

    def __init__(self, funcs):  # noqa: D107
        self.funcs = funcs

    def __call__(self, inputs):  # noqa: D102
        result = inputs
        for f in self.funcs:
            result = f(result)
        return result


class Fixer(Lookup):
    """Fixer class to look up fixes to apply to input dataset from the elastic search index.

    Gathers fixes into pre- and post-processors.
    Pre-process fixes are chained together to allow them to be executed with one call.
    """

    def __init__(self, dset):  # noqa: D107
        Lookup.__init__(self, dset)
        self._lookup_fix()

    def _gather_fixes(self, content):
        """Gather pre- and post-processing fixes together."""
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
        """Look up fixes on the elasticsearch index."""
        id = self._convert_id(self.dset)

        self.pre_processor = None
        self.pre_processors = []
        self.post_processors = []

        try:
            content = self.es.get(index=config_()["elasticsearch"]["fix_store"], id=id)
            self._gather_fixes(content)
        except exceptions.NotFoundError:
            pass
