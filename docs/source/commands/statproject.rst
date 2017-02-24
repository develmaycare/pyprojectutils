statproject
===========

Get information about a project.

.. code-block:: none

    usage: statproject [-h] [--cloc] [--color]
                       [--format= {csv,markdown,rst,stat,txt}]
                       [-p= PROJECT_HOME] [-v] [--version]
                       project_name

    positional arguments:
      project_name          The name of the project. The directory will be created
                            if it does not exist in $PROJECT_HOME

    optional arguments:
      -h, --help            show this help message and exit
      --cloc                Include information on lines of code. Takes longer to
                            run.
      --color               Highlight errors and warnings.
      --format= {csv,markdown,rst,stat,txt}
                            Output format. Defaults to plain stat.
      -p= PROJECT_HOME, --path= PROJECT_HOME
                            Path to where projects are stored. Defaults to
                            ~/Work
      -v                    Show version number and exit.
      --version             Show verbose version information and exit.


Generating a README
-------------------

The ``--format=markdown`` option produces output in `Markdown`_ format:

.. _Markdown: http://daringfireball.net/projects/markdown/

.. code-block:: bash

    cd example_project;
    statproject --format=markdown > README.markdown;

Although you'll likely want to customize the output, this is handy for
creating (or recreating) a README for the project.