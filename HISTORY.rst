Version History
===============

Unreleased
----------

Breaking Changes
^^^^^^^^^^^^^^^^
* In ``daops.utils.normalise`` ``ResultSet().file_paths`` has been changed to ``file_uris`` to allow file paths and
URLs to be collected.

New Features
^^^^^^^^^^^^
* ``daops.utils.core.is_characterised`` implemented - datasets are looked up in the character store.
* ``apply_fixes`` option now added to ``daops.ops.subset.subset``, ``daops.utils.normalise.normalise``
and ``daops.utils.core.open_dataset``. The default in all cases is to apply fixes (True).

Other Changes
^^^^^^^^^^^^^
* Changes to allow datasets without a time dimension to be processed.
* Use of ``DatasetMapper`` functions in ``daops.consolidate`` and ``daops.core`` to ensure all datasets are mapped to
ids/file paths correctly.

v0.3.0 (2020-11-19)
------------------

Updating doc strings and documentation.

Breaking Changes
^^^^^^^^^^^^^^^^
* ``clisops``>=0.4.0 and ``roocs-utils``>=0.1.4 used.
* ``data_refs`` parameter of ``daops.ops.subset.subset`` renamed to ``collection``.
* ``space`` parameter of ``daops.ops.subset.subset`` renamed to ``area``.
* ``chunk_rules`` parameter of ``daops.ops.subset.subset`` renamed to ``split_method``.
* ``filenamer`` parameter of ``daops.ops.subset.subset`` renamed to ``file_namer``.
* ``output_type`` parameter option added to ``daops.ops.subset.subset``.
* ``data_root_dir`` parameter in no longer needed ``daops.ops.subset.subset``.
* ``data_root_dir`` no longer a parameter of ``daops.utils.consolidate.consolidate``.


New Features
^^^^^^^^^^^^
* Added notebook with example usage.
* Config file now exists at ``daops.etc.roocs.ini``. This can be overwritten by setting the environment variable
  ``ROOCS_CONFIG`` to the file path of a config file.
* ``split_method`` implemented to split output files by if they exceed the memory limit provided in
  ``clisops.etc.roocs.ini`` named ``file_size_limit``.
  Currently only the ``time:auto`` exists which splits evenly on time ranges.
* ``file_namer`` implemented in subset operation. This has ``simple`` and ``standard`` options.
  ``simple`` numbers output files whereas ``standard`` names them according to the input dataset.
* Directories, file paths and dataset ids can now be used as inputs to the subset operation.
* Fixer class now looks up fixes on our elasticsearch index.

Other Changes
^^^^^^^^^^^^^
* Updated documentation.
* Functions that take the ``data_refs`` parameter have been changed to use ``collection`` parameter instead.
* Functions that take the ``data_ref`` parameter have been changed to use ``dset`` parameter instead.

v0.2.0 (2020-06-22)
------------------

* Updated to use clisops v0.2.0 (#17)
* Added xarray aggregation tests (#16)

v0.1.0 (2020-04-27)
------------------

* First release with clisops v0.1.0.
