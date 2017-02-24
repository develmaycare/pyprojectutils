enableproject
=============

Re-enable a project from hold or archive.

.. code-block:: none

    usage: enableproject [-h] [-p= PROJECT_HOME] [-v] [--version] project_name

    positional arguments:
      project_name          The name of the project to restore from hold or
                            archive.

    optional arguments:
      -h, --help            show this help message and exit
      -p= PROJECT_HOME, --path= PROJECT_HOME
                            Path to where projects are stored. Defaults to
                            ~/Work
      -v                    Show version number and exit.
      --version             Show verbose version information and exit.

.. note::
    This command is just a convenience for moving projects from hold or archive.
