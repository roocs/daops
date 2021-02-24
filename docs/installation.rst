.. highlight:: shell

============
Installation
============


Stable release
--------------
To install daops, run this command in your terminal:

.. code-block:: console

    $ pip install daops

This is the preferred method to install daops, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for daops can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/roocs/daops

Create Conda environment named `daops`:

.. code-block:: console

   $ conda env create -f environment.yml
   $ source activate daops

Install daops in development mode:

.. code-block:: console

  $ pip install -r requirements.txt
  $ pip install -r requirements_dev.txt
  $ python setup.py develop

Run tests:

.. code-block:: console

    $ pytest -v tests/

.. _Github repo: https://github.com/roocs/daops
