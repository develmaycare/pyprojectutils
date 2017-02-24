checkoutproject
===============

Check out a project from a source code repository.

.. code-block:: none

    usage: checkoutproject [-h] [-p= PROJECT_HOME] [-v] [--version]
                           project_name [provider]

    positional arguments:
      project_name          The name of the project. Typically, the directory name
                            in which the project is stored.
      provider              The SCM provider. This may be a base URL or one of
                            bitbucket or github.

    optional arguments:
      -h, --help            show this help message and exit
      -p= PROJECT_HOME, --path= PROJECT_HOME
                            Path to where projects are stored. Defaults to
                            ~/Work
      -v                    Show version number and exit.
      --version             Show verbose version information and exit.

.. note::
    Only Git repos are currently supported.

Provider is required the first time you run a checkout on the local machine. Afterward, the information is stored for
the project at ``$PROJECT_HOME/.repos/repo_name.ini``.

If ``bitbucket`` or ``github`` is specified, the ``BITBUCKET_USER`` or ``GITHUB_USER`` environment variables will be
used to assemble the URL.

You may also specify the ``DEFAULT_SCM`` environment variable to automatically use Bitbucket or GitHub. For example:

.. code-block:: bash

    export BITBUCKET_USER="develmaycare";
    export GITHUB_USER="develmaycare";
    export DEFAULT_SCM="github";

The ``DEFAULT_SCM`` itself defaults to GITHUB_USER.
