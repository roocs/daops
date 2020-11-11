
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
^^^^^^^^^^^

Report bugs at https://github.com/roocs/daops/issues.

If you are reporting a bug, please include:


* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
^^^^^^^^

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
^^^^^^^^^^^^^^^^^^

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
^^^^^^^^^^^^^^^^^^^

daops could always use more documentation, whether as part of the
official daops docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
^^^^^^^^^^^^^^^

The best way to send feedback is to file an issue at https://github.com/roocs/daops/issues.

If you are proposing a feature:


* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
^^^^^^^^^^^^

Ready to contribute? Here's how to set up ``daops`` for local development.


#. Fork the ``daops`` repo on GitHub.
#.
   Clone your fork locally:

    $ git clone git@github.com:your_name_here/daops.git

#.
   Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development:

    $ mkvirtualenv daops
    $ cd daops/
    $ python setup.py develop

#.
   Create a branch for local development:

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

#.
   When you are done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox:

    $ flake8 daops tests
    $ black --target-version py36 daops tests
    $ python setup.py test or py.test
    $ tox

   To get flake8, black and tox, just pip install them into your virtualenv.

#.
   Commit your changes and push your branch to GitHub:

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

#.
   Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:


#. The pull request should include tests.
#. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.md.
#. The pull request should work for Python 3.6, 3.7, 3.8, and 3.9. Check
   https://travis-ci.com/roocs/daops/pull_requests
   and make sure that the tests pass for all supported Python versions.
