lsprojects
==========

List projects managed on the local machine.

.. code-block:: none

    usage: lsprojects [-h] [-a] [--archive] [--branch] [--color] [--dirty] [-d]
                      [-f= CRITERIA] [--hold] [-p= PROJECT_HOME] [-v]
                      [--version]

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             Show projects even if there is no project.ini file.
      --archive             Only list projects that are staged for archiving.
      --branch              Show the current SCM branch name for each project.
      --color               Display the list in color-coded format.
      --dirty               Only show projects with dirty repos.
      -d, --disk            Calculate disk space. Takes longer to run.
      -f= CRITERIA, --filter= CRITERIA
                            Specify filter in the form of key:value. This may be
                            repeated. Use ? to list available values.
      --hold                Only list projects that are on hold.
      -p= PROJECT_HOME, --path= PROJECT_HOME
                            Path to where projects are stored. Defaults to
                            ~Work
      -v                    Show version number and exit.
      --version             Show verbose version information and exit.

Filtering
---------

Use the -f/--filter option to by most project attributes:

- category
- description (partial, case insensitive)
- name (partial, case insensitive)
- org (business/client code)
- scm
- tag
- type

The special --hold option may be used to list only projects that are on hold. See the holdproject command.

Format of INI
-------------

You can provide a ``project.ini`` file to provide detail on the project that
cannot be gleaned from the file system.

.. code-block:: ini

    [project]
    category = django
    description = A description of the project.
    status = development
    tags = CRM, Sales
    title = Project Title
    type = website

    [business]
    code = PTL
    name = Pleasant Tents, LLC

    [client]
    code = ACME
    name = ACME, Inc

    [domain]
    name = example
    tld = com

    [urls]
    docs = http://docs.example.net
    home = http://example.net
    issues = http://github.com/example/project/issues
    project = http://waffle.io/example/project
    scm = http://github.com/example/project

The ``tags``, ``type``, ``scope``, and ``status`` may be whatever you like.

Sections
--------

Attributes of ``[project]`` section are used as is. ``[business]`` and
``[client]`` are used to identify the beneficiary and/or developer of the
project.

Other sections may be added as you see fit. For example, the ``[domain]``
section above.

Tools and Links
...............

It can be useful to record the tools that are used for a project. Use the ``[urls]`` section to provide links to the
tools that you use. There are a number of recognized categories that may be specified:

- chat: The instant message tool used by developers.
- deploy: The tool you use for deployment.
- docs: The URL for documentation.
- help: End-user help.
- home: The official home page of the project or product.
- issues: The tracking tool for bugs, enhancements, etc.
- project: The project management tool.
- roadmap: The tool you use for the product roadmap, or the URL of the roadmap.
- scm: Source code management tool.

.. code-block:: ini

    [urls]
    docs = https://github.com/develmaycare/pyprojectutils/wiki
    issues = https://github.com/develmaycare/pyprojectutils/issues
    project = https://waffle.io/develmaycare/pyprojectutils
    roadmap = https://roadmunk.com

You can use environment variables and project variables as shortcuts:

.. code-block:: ini

    [urls]
    docs = https://github.com/%(GITHUB_USER)s/%(PROJECT_NAME)s/wiki
    issues = https://github.com/%(GITHUB_USER)s/%(PROJECT_NAME)s/issues
    project = https://waffle.io/%(GITHUB_USER)s/%(PROJECT_NAME)s
    roadmap = https://roadmunk.com

Finally, you may also use shortcuts for common services:

.. code-block:: ini

    [urls]
    docs = https://github.com/%(GITHUB_USER)s/%(project_name)s/wiki
    issues = %(GITHUB_ISSUES)s
    project = %(WAFFLE)s
    scm = %(GITHUB)s
    roadmap = https://roadmunk.com

Currently recognized:

- ``ANSIBLE`` is a link to the `Ansible documentation`_.
- ``BITBUCKET`` expands to the Bitbucket URL of the project.
- ``BITBUCKET_ISSUES`` expands to the Bitbucket issues URL of the project.
- ``GITHUB`` expands to the GitHub URL of the project.
- ``GITHUB_ISSUES`` expands to the GitHub issues URL of the project.
- ``PROJECT_NAME`` is the current project's name.
- ``WAFFLE`` is the URL for the project on `Waffle.io`_

.. _Ansible documentation: http://docs.ansible.com
.. _Waffle.io: http://waffle.io

Projects On Hold
----------------

The ``$PROJECT_HOME`` directory tends to build up a lot of projects, many of which are not active. You may place
projects on hold with the ``holdproject`` command or simply move the project to ``$PROJECTS_ON_HOLD``.

To display projects that are on hold, use the ``--hold`` option if ``lsprojects``.

Color Coding
------------

The ``--color`` option provides additional visual cues for the status of a project. The color is assigned in the
following order:

- red: An error occurred while finding or parsing project information.
- yellow: The project's repo is dirty.
- green: The project is live.
- cyan: The project has an unknown status.

HTML Output
-----------

The project list will be output when ``--format`` is ``html``. Use the ``--html-linked`` option to automatically create
links within the output. See below. The ``--html-wrapped`` creates a basic, but nice page from the output using Twitter
Bootstrap and Font Awesome.

The linking strategy for ``--html-linked`` uses the first valid link it finds to create the title as a link:

- ``docs/build/html/index.html``
- ``README.html``
- If ``project`` is set in the ``[urls]`` section, it will be used.
- If not other link is available, ``file://project_root`` is used.

All links are created with ``target="_blank"``.
