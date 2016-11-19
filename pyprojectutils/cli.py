from argparse import ArgumentParser, RawDescriptionHelpFormatter
import commands
from ConfigParser import RawConfigParser
import os
from datetime import datetime
import sys
from constants import ENVIRONMENTS, EXIT_OK, EXIT_OTHER, EXIT_USAGE, PROJECT_HOME
from library.projects import autoload_project, get_project_types, get_project_clients, get_project_statuses, \
    get_projects


def package_parser():
    """Parse a packages.ini file for a project."""

    __date__ = "2016-11-19"
    __help__ = """
#### Format of INI

The ``packages.ini`` contains a section for each package.

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

#### Output Formats

Several output formats are supported. All are sent to standard out unless a file is specified using ``--output``.

- ansible: For Ansible deployment.
- command: The install command.
- markdown: For Markdown.
- plain: For requirements files.
- rst: For ReStructuredText.
- table (default): Lists the packages in tabular format.

    """
    __version__ = "0.5.1-d"

    # Define options and arguments.
    parser = ArgumentParser(description=__doc__, epilog=__help__, formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument(
        "project_name",
        help="The name of the project."
    )

    parser.add_argument(
        "--env=",
        choices=ENVIRONMENTS,
        dest="env",
        help="Filter by environment."
    )

    parser.add_argument(
        "--format=",
        choices=("ansible", "command", "markdown", "plain", "rst", "table"),
        default="table",
        dest="output_format",
        help="Output format."
    )

    parser.add_argument(
        "--manager=",
        choices=("apt", "brew", "gem", "npm", "pip"),
        dest="manager",
        help="Filter by package manager."
    )

    parser.add_argument(
        "-O=",
        "--output=",
        dest="output_file",
        help="Path to the output file, if any."
    )

    parser.add_argument(
        "-p=",
        "--path=",
        default=PROJECT_HOME,
        dest="project_home",
        help="Path to where projects are stored. Defaults to %s" % PROJECT_HOME
    )

    # Access to the version number requires special consideration, especially
    # when using sub parsers. The Python 3.3 behavior is different. See this
    # answer: http://stackoverflow.com/questions/8521612/argparse-optional-subparser-for-version
    # parser.add_argument('--version', action='version', version='%(prog)s 2.0')
    parser.add_argument(
        "-v",
        action="version",
        help="Show version number and exit.",
        version=__version__
    )
    parser.add_argument(
        "--version",
        action="version",
        help="Show verbose version information and exit.",
        version="%(prog)s" + " %s %s" % (__version__, __date__)
    )

    # Parse arguments.
    args = parser.parse_args()

    # Load the project.
    project = autoload_project(args.project_name, args.project_home)
    if not project:
        print("Project not found: %s" % args.project_name)
        sys.exit(EXIT_OTHER)

    # Get dependencies.
    deps = project.get_dependencies()

    # Generate the output.
    output = list()
    if args.output_format == "ansible":
        if not args.manager:
            print("--manager is required for Ansible output.")
            sys.exit(EXIT_USAGE)

        output.append("- name: install %s requirements" % args.manager)
        output.append("  %s: name={{ item }} state=installed" % args.manager)

        a = list()
        for p in project.get_requirements(env=args.env, manager=args.manager):
            a.append('"%s"' % p.name)

        output.append("  with_items: [%s]" % ', '.join(a))
    elif args.output_format == "command":
        if not args.manager:
            print("--manager is required for command output.")
            sys.exit(EXIT_USAGE)

        for p in project.get_requirements(env=args.env, manager=args.manager):
            output.append(p.get_command())
    elif args.output_format == "markdown":
        output.append("## Requirements")
        output.append("")

        # By default we organize the markdown output around environment. This changes if the user has given us an env.
        if args.env:
            for p in project.get_requirements(env=args.env, manager=args.manager):
                output.append(p.to_markdown())
        else:
            for env in ENVIRONMENTS:
                output.append("### %s" % env)
                output.append("")

                for p in project.get_requirements(env=env, manager=args.manager):
                    output.append(p.to_markdown())
    elif args.output_format == "plain":
        output.append("# Generated by lspackages %s" % datetime.utcnow())

        if args.manager == "pip" and args.env != "base":
            output.append("-r base.pip")

        for p in project.get_requirements(env=args.env, manager=args.manager):
            output.append(p.to_plain())
    elif args.output_format == "rst":
        output.append("********")
        output.append("Packages")
        output.append("********")
        output.append("")

        # By default we organize the rst output around environment. This changes if the user has given us an env.
        if args.env:
            for p in project.get_requirements(env=args.env, manager=args.manager):
                output.append(p.to_rst())
        else:
            for env in ENVIRONMENTS:
                output.append(env)
                output.append("=" * len(env))
                output.append("")

                for p in project.get_requirements(env=env, manager=args.manager):
                    output.append(p.to_rst())
    else:
        output.append("=" * 105)
        output.append("%s Packages" % project.title)
        output.append("=" * 105)
        output.append(
            "%-40s %-10s %s"
            % ("Package", "Manager", "Environment")
        )
        output.append("-" * 105)

        for p in project.get_requirements(env=args.env):
            output.append(
                "%-40s %-10s %s"
                % (p.title, p.manager, ", ".join(p.env))
            )

    if args.output_file:
        result = write_file(args.output_file, "\n".join(output))
        if result:
            print("%s format written to %s." % (args.output_format, args.output_file))
        else:
            print("Could not write to: %s" % args.output_file)
            sys.exit(EXIT_OTHER)
    else:
        print("\n".join(output))

    sys.exit(EXIT_OK)


def project_parser():
    """Find, parse, and collect project information."""

    __date__ = "2016-11-18"
    __help__ = """
#### Format of INI

You can provide a ``project.ini`` file to provide detail on the project that
cannot be gleaned from the file system.

    [project]
    description = A description of the project.
    scope = website
    status = development
    tags = CRM, Sales
    type = django
    title = Project Title

    [business]
    code = PTL
    name = Pleasant Tents, LLC

    [client]
    code = ACME
    name = ACME, Inc

    [domain]
    name = example
    tld = com

The ``tags``, ``type``, ``scope``, and ``status`` may be whatever you like.

#### Sections

Attributes of ``[project]`` section are used as is. ``[business]`` and
``[client]`` are used to identify the beneficiary and/or developer of the
project.

Other sections may be added as you see fit. For example, the ``[domain]``
section above.

#### Additional Data

Additional data may be displayed in the list output and when using the
``--name`` switch.

- The SCM and disk usage of the project may be automatically determined.
- The project tree is obtained with the ``tree`` command.

#### Generating a README

The ``--name`` switch searches for a specific project and (if found) outputs
project information in [Markdown][markdown] format:

[markdown]: http://daringfireball.net/projects/markdown/

    cd example_project;
    lsprojects --name=example_project > README.markdown;

Although you'll likely want to customize the output, this is handy for
creating (or recreating) a README for the project.

"""
    __version__ = "1.0.0-d"

    # Define options and arguments.
    parser = ArgumentParser(description=__doc__, epilog=__help__, formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        dest="show_all",
        help="Show projects even if there is no project.ini"
    )

    parser.add_argument(
        "-c=",
        "--client=",
        dest="client_code",
        help="Filter by client organization. Use ? to list organizations"
    )

    parser.add_argument(
        "--dirty",
        action="store_true",
        dest="show_dirty",
        help="Only show projects with dirty repos"
    )

    parser.add_argument(
        "-d",
        "--disk",
        action="store_true",
        dest="include_disk",
        help="Calculate disk space. Takes longer to run."
    )

    parser.add_argument(
        "-n=",
        "--name=",
        dest="project_name",
        help="Find a project by name and display it's information."
    )

    parser.add_argument(
        "-p=",
        "--path=",
        default=PROJECT_HOME,
        dest="project_home",
        help="Path to where projects are stored. Defaults to %s" % PROJECT_HOME
    )

    parser.add_argument(
        "-s=",
        "--status=",
        dest="status",
        help="Filter by project status. Use ? to list available statuses."
    )

    parser.add_argument(
        "-t=",
        "--type=",
        dest="project_type",
        help="Filter by project type. Use ? to list available types."
    )

    # Access to the version number requires special consideration, especially
    # when using sub parsers. The Python 3.3 behavior is different. See this
    # answer: http://stackoverflow.com/questions/8521612/argparse-optional-subparser-for-version
    # parser.add_argument('--version', action='version', version='%(prog)s 2.0')
    parser.add_argument(
        "-v",
        action="version",
        help="Show version number and exit.",
        version=__version__
    )
    parser.add_argument(
        "--version",
        action="version",
        help="Show verbose version information and exit.",
        version="%(prog)s" + " %s %s" % (__version__, __date__)
    )

    args = parser.parse_args()

    # Handle project by name requests.
    if args.project_name:
        project = autoload_project(args.project_name, include_disk=args.include_disk, path=args.project_home)

        if not project.load(include_disk=args.include_disk):
            print("Could not autoload the project: %s" % args.project_name)
            sys.exit(EXIT_OTHER)

        print(project.to_markdown())

        sys.exit(EXIT_OK)

    # Get the available types.
    project_types = get_project_types(args.project_home)

    # List the clients as requested.
    if args.client_code == "?":
        for c in get_project_clients(args.project_home):
            print(c)

        sys.exit(EXIT_OK)

    # List the status as requested.
    if args.status == "?":
        status_list = get_project_statuses(args.project_home)
        for s in status_list:
            print(s)

        sys.exit(EXIT_OK)

    # List the types as requested.
    if args.project_type == "?":
        for t in project_types:
            print(t)

        sys.exit(EXIT_OK)

    # Print the report heading.
    heading = "Projects"
    if args.project_type:
        heading += "(%s)" % args.project_type

    print "=" * 105
    print heading
    print "=" * 105

    # Print the column headings.
    if args.project_type:
        print "%-40s %-10s %-11s %-10s %-5s %-4s" % ("Title", "Client", "Version", "Status", "Disk", "SCM")
    else:
        print "%-40s %-10s %-10s %-10s %-11s %-10s %-4s" % (
        "Title", "Type", "Client", "Version", "Status", "Disk", "SCM")

    print "-" * 105

    # Build the criteria.
    criteria = dict()

    if args.client_code:
        criteria['org'] = args.client_code

    if args.show_dirty:
        criteria['is_dirty'] = True

    if args.status:
        criteria['status'] = args.status

    if args.project_type:
        criteria['type'] = args.project_type

    # Print the rows.
    projects = get_projects(
        args.project_home,
        criteria=criteria,
        include_disk=args.include_disk,
        show_all=args.show_all
    )

    if len(projects) == 0:
        print ""
        print "No results."
        sys.exit(EXIT_OK)

    for p in projects:

        if len(p.title) > 40:
            title = p.title[:37] + "..."
        else:
            title = p.title

        if p.config_exists:
            config_exists = ""
        else:
            config_exists = "*"

        if p.is_dirty:
            scm = "%s+" % p.scm
        else:
            scm = p.scm

        if args.project_type:
            print "%-40s %-10s %-10s %-11s %-5s %-4s %-1s" % (title, p.org, p.version, p.status, p.disk, p.scm, config_exists)
        else:
            print "%-40s %-10s %-10s %-10s %-11s %-10s %-4s %-1s" % (title, p.type, p.org, p.version, p.status, p.disk, scm, config_exists)

    if len(projects) == 1:
        label = "result"
    else:
        label = "results"

    print "-" * 105
    print ""
    print "%s %s." % (len(projects), label)

    if args.show_all:
        print "* indicates absence of project.ini file."

    # Quit.
    sys.exit(EXIT_OK)


def write_file(path, content):
    """Write to a file in a memory-safe way.

    :param path: Path to the file.
    :type path: str

    :param content: Content of the file.
    :type content: str

    :rtype: bool
    :returns: ``True`` if the file could be written.

    """
    try:
        with open(path, "wb") as f:
            f.write(content)
            f.close()
        return True
    except IOError:
        return False
