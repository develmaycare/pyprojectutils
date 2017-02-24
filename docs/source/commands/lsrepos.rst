lsrepos
=======

List source code repos that have been discovered by the checkoutproject command.

..  code-block:: none

    usage: lsrepos [-h] [-a] [-f= CRITERIA] [--hold] [-v] [--version]

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             List all (even remote) repos.
      -f= CRITERIA, --filter= CRITERIA
                            Specify filter in the form of key:value. This may be
                            repeated. Use ? to list available values.
      --hold                Only list projects that are on hold.
      -v                    Show version number and exit.
      --version             Show verbose version information and exit.

Filtering
---------

Use the -f/--filter option to by most project attributes:

- name (partial, case insensitive)
- project
- host (bitbucket, bb, github, gh)
- type (git, hg, svn)
- user