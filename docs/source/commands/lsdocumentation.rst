lsdocumentation
===============

Find, parse, and collect documentation information.

We use the excellent `Dash`_ app for documentation, but some documentation is nice to have on the local machine.
This may even be extended to cover training materials, e-books, etc.

.. _Dash: https://kapeli.com/dash

.. code-block:: none

    usage: lsdocumentation [-h] [-a] [-d] [-f= CRITERIA]
                           [-p= DOCUMENTATION_HOME] [-v] [--version]

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             Show documentation even if there is no info.ini file.
      -d, --disk            Calculate disk space. Takes longer to run.
      -f= CRITERIA, --filter= CRITERIA
                            Specify filter in the form of key:value. This may be
                            repeated. Use ? to list available values.
      -p= DOCUMENTATION_HOME, --path= DOCUMENTATION_HOME
                            Path to the documentation library. Defaults to
                            ~/Dropbox/Business/Documentation
      -v                    Show version number and exit.
      --version             Show verbose version information and exit.


Filtering
---------

Use the -f/--filter option to by most project attributes:

- author (partial, case insensitive)
- category
- description (partial, case insensitive)
- name (partial, case insensitive)
- publisher (partial, case insensitive)
- tag
- type

