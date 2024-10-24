============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/roocs/daops/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

daops could always use more documentation, whether as part of the
official daops docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/roocs/daops/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `daops` for local development.

1. Fork the `daops` repo on GitHub.

2. Clone your fork locally::

    $ git clone git@github.com:your-name/daops.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    # For virtualenv environments:
    $ mkvirtualenv daops

    # For Anaconda/Miniconda environments:
    $ conda create -n daops python=3.6

    $ cd daops/
    $ pip install -e .

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally!

5. When you're done making changes, check that you verify your changes with `black` and run the tests, including testing other Python versions with `tox`::

    # For virtualenv environments:
    $ pip install black pytest tox

    # For Anaconda/Miniconda environments:
    $ conda install -c conda-forge black pytest tox

    $ black daops tests
    $ python setup.py test
    $ tox

6. Before committing your changes, we ask that you install `pre-commit` in your virtualenv. `Pre-commit` runs git hooks that ensure that your code resembles that of the project and catches and corrects any small errors or inconsistencies when you `git commit`::

    # For virtualenv environments:
    $ pip install pre-commit

    # For Anaconda/Miniconda environments:
    $ conda install -c conda-forge pre_commit

    $ pre-commit install

7. Commit your changes and push your branch to GitHub::

    $ git add *

    $ git commit -m "Your detailed description of your changes."
    # `pre-commit` will run checks at this point:
    # if no errors are found, changes will be committed.
    # if errors are found, modifications will be mades. Simply `git commit` again.

    $ git push origin name-of-your-bugfix-or-feature

8. Submit a pull request through the GitHub website.

Logging
-------

``daops`` uses the `loguru <https://loguru.readthedocs.io/en/stable/index.html>`_ library as its primary logging engine. In order to integrate this kind of logging in processes, we can use their logger:

.. code-block:: python

    from loguru import logger

    logger.warning("This a warning message!")

The mechanism for enabling log reporting in scripts/notebooks using ``loguru`` is as follows:

.. code-block:: python

    import sys
    from loguru import logger

    logger.enable("clisops")
    LEVEL = "INFO || DEBUG || WARNING || etc."
    logger.add(sys.stdout, level=LEVEL)  # for logging to stdout
    # or
    logger.add("my_log_file.log", level=LEVEL, enqueue=True)  # for logging to a file

For convenience, a preset logger configuration can be enabled via `daops.enable_logging()`.

.. code-block:: python

    from daops import enable_logging

    enable_logging()

Pull Request Guidelines
-----------------------

Before you submit a pull request, please follow these guidelines:

1. Open an *issue* on our `GitHub repository`_ with your issue that you'd like to fix or feature that you'd like to implement.
2. Perform the changes, commit and push them either to new a branch within roocs/daops or to your personal fork of daops.

.. warning::
     Try to keep your contributions within the scope of the issue that you are addressing.
     While it might be tempting to fix other aspects of the library as it comes up, it's better to
     simply to flag the problems in case others are already working on it.

     Consider adding a "**# TODO:**" comment if the need arises.

3. Pull requests should raise test coverage for the daops library. Code coverage is an indicator of how extensively tested the library is.
   If you are adding a new set of functions, they **must be tested** and **coverage percentage should not significantly decrease.**
4. If the pull request adds functionality, your functions should include docstring explanations.
   So long as the docstrings are syntactically correct, sphinx-autodoc will be able to automatically parse the information.
   Please ensure that the docstrings adhere to one of the following standards:

   * `numpydoc`_
   * `reStructuredText (ReST)`_

5. The pull request should work for Python 3.6, 3.7 and 3.8 as well as raise test coverage.
   Pull requests are also checked for documentation build status and for `PEP8`_ compliance.

   The build statuses and build errors for pull requests can be found at:
    https://travis-ci.org/roocs/daops/pull_requests

.. warning::
    PEP8 and Black is strongly enforced. Ensure that your changes pass **Flake8** and **Black**
    tests prior to pushing your final commits to your branch. Code formatting errors are treated
    as build errors and will block your pull request from being accepted.


.. _`numpydoc`: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
.. _`reStructuredText (ReST)`: https://www.jetbrains.com/help/pycharm/using-docstrings-to-specify-types.html
.. _`GitHub Repository`: https://github.com/roocs/daops
.. _`PEP8`: https://www.python.org/dev/peps/pep-0008/
