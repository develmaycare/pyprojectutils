statdocumentation
=================

Display information on a specific set of documentation.

.. code-block:: none

    usage: statdocumentation [-h] [-d] [--format= [{markdown,plain}]]
                             [-p= DOCUMENTATION_HOME] [-v] [--version]
                             documentation_name

    positional arguments:
      documentation_name    The title or name of the work.

    optional arguments:
      -h, --help            show this help message and exit
      -d, --disk            Calculate disk space. Takes longer to run.
      --format= [{markdown,plain}]
                            Choose the format of the output.
      -p= DOCUMENTATION_HOME, --path= DOCUMENTATION_HOME
                            Path to the documentation library. Defaults to
                            $DOCUMENTATION_HOME
      -v                    Show version number and exit.
      --version             Show verbose version information and exit.

Name may be partially matched and is case insensitive.
