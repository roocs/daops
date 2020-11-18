Version History
===============

v0.3.0 (2020-11-16)
------------------

Updating doc strings and documentation.

Breaking Changes
^^^^^^^^^^^^^^^^
* ``chunk_rules`` parameter of ``clisops.ops.subset`` renamed to ``split_method``.
* ``filenamer`` parameter of ``clisops.ops.subset`` renamed to ``file_namer``.

New Features
^^^^^^^^^^^^
* Added notebooks with example usage.
* Config file now exists at ``daops.etc.roocs.ini``. This can be overwritten by setting the environment variable
  ``ROOCS_CONFIG`` to the file path of a config file.
* ``split_method`` implemented to split output files by if they exceed the memory limit provided in
  ``clisops.etc.roocs.ini`` named ``file_size_limit``.
  Currently only the ``time:auto`` exists which splits evenly on time ranges.
* ``file_namer`` implemented in ``clisops.ops.subset``. This has ``simple`` and ``standard`` options.
  ``simple`` numbers output files whereas ``standard`` names them according to the input dataset.

Other Changes
^^^^^^^^^^^^^
* Updated documentation.
* Removed udunits as a requirement.
* rtee and libspatialindex remove as requirements, making it easier to install through pip.

v0.2.0 (2020-06-22)
------------------

* Updated to use clisops v0.2.0 (#17)
* Added xarray aggregation tests (#16)

v0.1.0 (2020-04-27)
------------------

* First release with clisops v0.1.0.
