lsdependencies
==============

List the packages for a given project.

.. code-block:: none

    usage: lspackages [-h]
                      [--env= {base,control,development,testing,staging,live}]
                      [--format= {ansible,command,markdown,plain,rst,table}]
                      [--manager= {apt,brew,gem,npm,pip}] [-O= OUTPUT_FILE]
                      [-p= PROJECT_HOME] [-v] [--version]
                      project_name

    positional arguments:
      project_name          The name of the project.

    optional arguments:
      -h, --help            show this help message and exit
      --env= {base,control,development,testing,staging,live}
                            Filter by environment.
      --format= {ansible,command,markdown,plain,rst,table}
                            Output format.
      --manager= {apt,brew,gem,npm,pip}
                            Filter by package manager.
      -O= OUTPUT_FILE, --output= OUTPUT_FILE
                            Path to the output file, if any.
      -p= PROJECT_HOME, --path= PROJECT_HOME
                            Path to where projects are stored. Defaults to
                            ~/Work
      -v                    Show version number and exit.
      --version             Show verbose version information and exit.

Location of the INI
-------------------

The command will look for the ``packages.ini`` file in these locations within project root:

1. ``deploy/requirements/packages.ini``
2. ``requirements/packages.ini``
3. ``requirements.ini``

Format of INI
-------------

The ``packages.ini`` contains a section for each package.

.. code-block:: ini

    [package_name]
    ...

The following options are recognized:

- branch: The branch to use when downloading the package. Not supported by all package managers.
- cmd: The install command. This is generated automatically unless this option is given.
- docs: The URL for package documentation.
- egg: The egg name to use for a Python packackage install.
- env: The environment where this package is used.
- home: The URL for the package home page.
- manager: The package manager to use. Choices are apt, brew, gem, npm, and pip.
- note: Any note regarding the package. For example, how or why you are using it.
- scm: The URL for the package's source code management tool.
- title: A title for the package.
- version: The version spec to use for installs. For example: ``>=1.10``

Output Formats
--------------

Several output formats are supported. All are sent to standard out unless a file is specified using ``--output``.

- ansible: For Ansible deployment.
- command: The install command.
- markdown: For Markdown.
- plain: For requirements files.
- rst: For ReStructuredText.
- table (default): Lists the packages in tabular format.
