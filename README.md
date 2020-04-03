# daops - data-aware operations


[![Pypi](https://img.shields.io/pypi/v/daops.svg)](https://pypi.python.org/pypi/daops)

[![Travis](https://img.shields.io/travis/ellesmith88/daops.svg)](https://travis-ci.org/ellesmith88/daops)

[![Documentation](https://readthedocs.org/projects/daops/badge/?version=latest)](https://daops.readthedocs.io/en/latest/?badge=latest)

The `daops` library (pronounced "day-ops") provides a python interface to a 
set of operations suitable for working with climate simulation outputs. It is 
typically used with ESGF data sets that are described in NetCDF files. `daops` 
is unique in that it accesses a store of _fixes_ defined for data sets that are 
irregular when compared with others in their _population_. 

When a `daops` operation, such as `subset`, is requested, the library will look 
up a database of known fixes before performing and calculations or transformations. 
The data will be loaded and _fixed_ using the [xarray](http://xarray.pydata.org/) 
library before the any actual operations are sent to its sister library 
[clisops](https://github.com/roocs/clisops). 

* Free software: BSD
* Documentation: https://daops.readthedocs.io

## Features

The package has the following features:
 * Ability to run _data-reduction_ operations on large climate data sets.
 * Knowledge of irregularities/anomalies in some climate data sets.
 * Ability to apply _fixes_ to those data sets before operating on them. 
 This process is called _normalisation_ of the data sets.

# Credits

This package was created with `Cookiecutter` and the `cedadev/cookiecutter-pypackage` project template.

 * Cookiecutter: https://github.com/audreyr/cookiecutter
 * cookiecutter-pypackage: https://github.com/cedadev/cookiecutter-pypackage
