holdproject
===========

Place a project on hold.

.. code-block:: none

    usage: holdproject [-h] [--force] [-p= PROJECT_HOME] [-v] [--version]
                       project_name

    positional arguments:
      project_name          The name of the project to place on hold.

    optional arguments:
      -h, --help            show this help message and exit
      --force               Hold the project even if the repo is dirty.
      -p= PROJECT_HOME, --path= PROJECT_HOME
                            Path to where projects are stored. Defaults to
                            ~/Work
      -v                    Show version number and exit.
      --version             Show verbose version information and exit.

This does a couple of things for you:

- It checks to see if there are uncommitted changes and by default prevents moving the project if the repo is dirty.
- It moves the project to ``$PROJECTS_ON_HOLD`` which defaults to ``$PROJECT_HOME/.hold/``.
