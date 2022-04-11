Version History
===============

v0.8.0 (2022-04-13)
-------------------

New Features
^^^^^^^^^^^^

* Added `AverageTime` operation.
* Added support for decadal fixes (#89, #87, #84, #83).


v0.7.0 (2021-10-28)
-------------------
Breaking Changes
^^^^^^^^^^^^^^^^
* ``clisops``>=0.7.0 and ``roocs-utils``>=0.5.0 required.
* ``fsspec`` no longer constrained to ``fsspec`` < 0.9
* Python 3.7 required.
* ``time`` input for ``time`` in ``ops.subset.subset`` but now be one of [<class 'roocs_utils.parameter.param_utils.Interval'>, <class 'roocs_utils.parameter.param_utils.Series'>, <class 'NoneType'>, <class 'str'>].
* ``level`` input for ``level`` in ``ops.subset.subset`` but now be one of [<class 'roocs_utils.parameter.param_utils.Interval'>, <class 'roocs_utils.parameter.param_utils.Series'>, <class 'NoneType'>, <class 'str'>].

New Features
^^^^^^^^^^^^
* ``time_components`` argument added to ``ops.subset.subset`` to allowing subsetting by time components such as year, month, day etc.

Other Changes
^^^^^^^^^^^^^
* Python 3.6 no longer tested in GitHub actions.

v0.6.0 (2021-05-19)
-------------------
Breaking Changes
^^^^^^^^^^^^^^^^
* intake, fsspec<0.9 and aiohttp are new dependencies in order to use the intake catalog search functionality.
* ``clisops``>=0.6.4 and ``roocs-utils``>=0.4.2 required.

New Features
^^^^^^^^^^^^
* Intake catalog search functionality added. In use in ``utils.consolidate``: if the catalog is used for the project, then consolidate will find the files within the time range specified using the intake catalog, rather than opening xarray datasets.
* ``intake_catalog_url`` has been added to ``etc/roocs.ini``

v0.5.0 (2021-02-26)
------------------

New Features
^^^^^^^^^^^^
* ``average_over_dims`` added in ``daops.ops.average``.

Other Changes
^^^^^^^^^^^^^
* Refactoring of daops.ops.subset to use a base ``Operation`` class in ``daops.ops.base``


v0.4.0 (2021-02-23)
------------------

Breaking Changes
^^^^^^^^^^^^^^^^
* In ``daops.utils.normalise`` ``ResultSet().file_paths`` has been changed to ``file_uris`` to allow file paths and URLs to be collected.
* ``clisops``>=0.6.1 and ``roocs-utils``>=0.2.1 used.
* New dev dependency: GitPython==3.1.12
* ``consolidate_dset`` has been removed in ``daops.utils.consolidate`` as ``dset_to_filepaths`` from ``roocs_utils.project_utils`` is now used to find the file paths.

New Features
^^^^^^^^^^^^
* ``daops.utils.core.is_characterised`` implemented - datasets are looked up in the character store.
* ``apply_fixes`` option now added to ``daops.ops.subset.subset``, ``daops.utils.normalise.normalise`` and ``daops.utils.core.open_dataset``. The default in all cases is to apply fixes (True).

Other Changes
^^^^^^^^^^^^^
* Changes to allow datasets without a time dimension to be processed.
* Swapped from travis CI to GitHub actions
* Test data no longer a submodule - the data is retrieved from GitHub when the tests are run.
* Use of ``DatasetMapper`` functions in ``daops.consolidate`` and ``daops.core`` to ensure all datasets are mapped to ids/file paths correctly.


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
