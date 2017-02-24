bumpversion
===========

Increment the version number immediately after checking out a release branch.

.. code-block:: none

    usage: bumpversion [-h] [-b= BUILD] [-M] [-m] [-n= NAME] [-p] [-P= PATH]
                      [--preview] [-s= STATUS] [-T= TEMPLATE] [-v] [--version]
                      [project_name]

    positional arguments:
      project_name          The name of the project. Typically, the directory name
                            in which the project is stored.

    optional arguments:
      -h, --help            show this help message and exit
      -b= BUILD, --build= BUILD
                            Supply build meta data.
      -M, --major           Increase the major version number when you make
                            changes to the public API that are backward-
                            incompatible.
      -m, --minor           Increase the minor version number when new or updated
                            functionality has been implemented that does not
                            change the public API.
      -n= NAME, --name= NAME
                            Name your release.
      -p, --patch           Increase the patch level when backward-compatible bug-
                            fixes have been implemented.
      -P= PATH, --path= PATH
                            The path to where projects are stored. Defaults to
                            ~/Work
      --preview             Preview the output, but don't make any changes.
      -s= STATUS, --status= STATUS
                            Use the status to denote a pre-release version.
      -T= TEMPLATE, --template= TEMPLATE
                            Path to the version.py template you would like to use.
                            Use ? to see the default.
      -v                    Show version number and exit.
      --version             Show verbose version information and exit.


.. tip::
    If you omit the ``project_name`` then ``bumpversion`` will attempt to locate the ``VERSION.txt`` file to
    automatically determine the current project name based on your current working diretory.

When to Use
-----------

Generally, you want to increment the version number immediately after checking out a release branch. However, you may
wish to bump the version any time during development, especially during early development where the MINOR and PATCH
versions are changing frequently.

Here is an example workflow:

.. code-block:: bash

    # Get the current version and check out the next release.
    bumpversion myproject; # get the current version, example 1.2
    git checkout -b release-1.3;

    # Bump automatically sets the next minor version with a status of d.
    bumpversion myproject -m -s d;

    # Commit the bump.
    git commit -am "Version Bump";

    # Go do the final work for the release.
    # ...

    # Merge the release.
    git checkout master;
    git merge --no-ff release-1.3;
    git tag -a 1.3;

    # Merge back to development.
    git checkout development;
    git merge --no-ff release-1.3;

Semantic Versioning
-------------------

This utility makes use of `Semantic Versioning`_. From the documentation:

1. MAJOR version when you make incompatible API changes,
2. MINOR version when you add functionality in a backwards-compatible manner, and
3. PATCH version when you make backwards-compatible bug fixes.

Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.

.. _Semantic Versioning: http://semver.org

Status
......

We define the following status codes:

- ``x`` Prototype, experimental. Use at your own risk.
- ``p`` Planning, specification, not even in development.
- ``d`` Development. Unstable, untested.
- ``a`` Feature complete.
- ``b`` Ready for testing and QA.
- ``r`` Release candidate.
- ``o`` Obsolete, deprecated, or defect. End of life.

You may of course use whatever status you like.

Release Versus Version
----------------------

Release
.......

A *release* is a collection of updates representing a new version of the product. A release is represented by the full
string of MAJOR.MINOR.PATCH, and may optionally include the status and build until the release is live.

The release is probably never displayed to Customers or Users.

Version
.......

A *version* represents a specific state of the product. The version is represented by the MAJOR.MINOR string of the
release.

The version may be shown to Customers or Users.
