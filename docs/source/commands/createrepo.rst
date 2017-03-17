createrepo
==========

Create a (remote) source code repo.

.. code-block:: none

    usage: createrepo [-h] [-D= DESCRIPTION] [--host= {bitbucket,bb,github,gh}]
                      [-I] [-P] [-v] [--version]
                      [repo_name]

    positional arguments:
      repo_name             The name of the repo. This defaults to the current
                            directory name.

    optional arguments:
      -h, --help            show this help message and exit
      -D= DESCRIPTION, --description= DESCRIPTION
                            The description. Defaults to the contents of the
                            DESCRIPTION.txt file if one is present.
      --host= {bitbucket,bb,github,gh}
                            The SCM provider. The abbreviation and full name are
                            supported as shown. Defaults to the DEFAULT_SCM
                            environment variable.
      -I, --issues          Indicates issues should be enabled for the repo.
      -P, --private         Indicates the repo is private.
      -v                    Show version number and exit.
      --version             Show verbose version information and exit.


.. note::
    Only Git repos are currently supported.

You may also specify the ``DEFAULT_SCM`` environment variable to automatically use a recognized host. The user and
password are also required. For example:

.. code-block:: bash

    export DEFAULT_SCM="github";
    export GITHUB_USER="develmaycare";
    export GITHUB_PASS="asdf1234";
