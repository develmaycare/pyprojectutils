archiveproject
==============

Place a project in the archive.

.. code-block:: none

    usage: archiveproject [-h] [--force] [-p= PROJECT_HOME] [-v] [--version] project_name

    positional arguments:
      project_name          The name of the project to archive.

    optional arguments:
      -h, --help            show this help message and exit
      --force               Archive the project even if the repo is dirty. Be
                            careful!
      -p= PROJECT_HOME, --path= PROJECT_HOME
                            Path to where projects are stored. Defaults to
                            ~/Work
      -v                    Show version number and exit.
      --version             Show verbose version information and exit.

.. note::
    We first check to see if the repo is dirty and by default the project cannot be placed in the archive without first
    committing the changes.
