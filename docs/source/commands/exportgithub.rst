exportgithub
============

Export Github milestones and issues.

.. code-block:: none

    usage: exportgithub [-h] [--format= {csv,html,markdown,rst,txt}]
                        [-L= LABELS] [-v] [--version]
                        repo_name [output_file]

    positional arguments:
      repo_name             Name of the repository.
      output_file           The file (or path) to which data should be exported.
                            If omitted, the export goes to STDOUT.

    optional arguments:
      -h, --help            show this help message and exit
      --format= {csv,html,markdown,rst,txt}
                            Output format. Defaults to CSV.
      -L= LABELS, --label= LABELS
                            Filter for a specific label.
      -v                    Show version number and exit.
      --version             Show verbose version information and exit.


Environment Variables
---------------------

``GITHUB_USER`` and ``GITHUB_PASSWORD`` must be set in your console environment.

Issue Status
------------

We look for labels of ``ready``, ``in progress``, ``on hold``, and ``review ``to determine the issue's current position
in the workflow.

Output Formats
--------------

CSV (Roadmunk)
..............

The default output (CSV) may be further parsed by your own scripts. However, it was created to conform with the
excellent `Roadmunk`_ application, which is like a Swiss army knife for displaying road map data.

.. _Roadmunk: http://roadmunk.com

HTML
....

HTML output is for `Bootstrap 3`_ and includes classes for ``table-bordered`` and ``table-striped``. If you don't want
this, use the ``--no-header`` switch.

.. _Bootstrap 3: http://getbootstrap.com

Markdown
........

Markdown output uses the format for the ``pipe_tables`` extension of `Pandoc`_. The output is *not* pretty, but should
parse well using Pandoc.

.. _Pandoc: http://pandoc.org/MANUAL.html#tables

ReStructuredText
................

ReStructuredText output uses the `csv-table`_ directive.

.. _csv-table: http://docutils.sourceforge.net/docs/ref/rst/directives.html#id4

Text
....

The final format available is plain text. This simply outputs the issue title, the URL, and a line feed for each issue.
This is useful for creating a ``TODO.txt`` file.
