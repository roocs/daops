
daops - data-aware operations
=============================


.. image:: https://img.shields.io/pypi/v/daops.svg
   :target: https://pypi.python.org/pypi/daops
   :alt: Pypi



.. image:: https://github.com/roocs/daops/workflows/build/badge.svg
    :target: https://github.com/roocs/daops/actions
    :alt: Build Status



.. image:: https://readthedocs.org/projects/daops/badge/?version=latest
   :target: https://daops.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation


The ``daops`` library (pronounced "day-ops") provides a python interface to a
set of operations suitable for working with climate simulation outputs. It is
typically used with ESGF data sets that are described in NetCDF files. ``daops``
is unique in that it accesses a store of *fixes* defined for datasets that are
irregular when compared with others in their *population*.

When a ``daops`` operation, such as ``subset``\ , is requested, the library will look
up a database of known fixes before performing and calculations or transformations.
The data will be loaded and *fixed* using the `xarray <http://xarray.pydata.org/>`_
library before the any actual operations are sent to its sister library
`clisops <https://github.com/roocs/clisops>`_.


* Free software: BSD
* Documentation: https://daops.readthedocs.io

Features
--------

The package has the following features:


* Ability to run *data-reduction* operations on large climate data sets.
* Knowledge of irregularities/anomalies in some climate data sets.
* Ability to apply *fixes* to those data sets before operating on them.
  This process is called *normalisation* of the data sets.

Credits
=======

This package was created with ``Cookiecutter`` and the ``cedadev/cookiecutter-pypackage`` project template.


* Cookiecutter: https://github.com/audreyr/cookiecutter
* cookiecutter-pypackage: https://github.com/cedadev/cookiecutter-pypackage


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/python/black
   :alt: Python Black
