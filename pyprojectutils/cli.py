from argparse import ArgumentParser, RawDescriptionHelpFormatter
from datetime import datetime
import sys
from library.constants import BASE_ENVIRONMENT, ENVIRONMENTS, EXIT_OK, EXIT_INPUT, EXIT_OTHER, EXIT_USAGE, PROJECT_HOME
from library.exceptions import OutputError
from library.projects import autoload_project, get_project_types, get_project_clients, get_project_statuses, \
    get_projects, initialize_project, Project
from library.passwords import RandomPassword
from library.releases import Version
from library.shortcuts import parse_template, write_file


def generate_password():
    """Generate a random password."""

    __author__ = "Shawn Davis <shawn@ptltd.co>"
    __date__ = "2016-11-19"
    __help__ = """
We often need to generate passwords automatically. This utility does just
that. Install pyprojectutils it during deployment to create passwords on the fly.
    """
    __version__ = "0.10.1-d"

    # Define options and arguments.
    parser = ArgumentParser(description=__doc__, epilog=__help__, formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument(
        "--format=",
        choices=["crypt", "md5", "plain", "htpasswd"],
        default="plain",
        dest="format",
        help="Choose the format of the output.",
        nargs="?"
    )
    parser.add_argument("--strong", action="store_true", help="Make the password stronger.")
    parser.add_argument(
        "-U",
        action="store_true",
        dest="use_unambiguous",
        help="Avoid ambiguous characters."
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

    # This will display help or input errors as needed.
    args = parser.parse_args()
    # print args

    password_length = 10
    if args.strong:
        password_length = 20

    password = RandomPassword(password_length, use_unambiguous=args.use_unambiguous)

    if args.format == "crypt":
        print(password.to_crypt())
    elif args.format == "htpasswd":
        print(password.to_htpasswd())
    elif args.format == "md5":
        print(password.to_md5())
    else:
        print(password.plain_text)

    # Quit.
    sys.exit(EXIT_OK)


def package_parser():
    """Parse a packages.ini file for a project."""

    __date__ = "2016-11-19"
    __help__ = """
#### Location of the INI

The command will look for the ``packages.ini`` file in these locations within project root:

1. ``deploy/requirements/packages.ini``
2. ``requirements/packages.ini``
3. ``requirements.ini``

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

        if args.manager == "pip" and args.env != BASE_ENVIRONMENT:
            output.append("-r base.pip")

        for p in project.get_requirements(env=args.env, manager=args.manager):
            try:
                output.append(p.to_plain())
            except OutputError, e:
                print(e)
                sys.exit(EXIT_OTHER)
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
        try:
            result = write_file(args.output_file, "\n".join(output))
        except OutputError, e:
            print(e)
            sys.exit(EXIT_OTHER)
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

    __date__ = "2016-12-08"
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
    __version__ = "1.1.4-d"
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
        "--init",
        action="store_true",
        dest="initialize_project",
        help="Initialize project meta files. Project name is required."
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

    # Initialize a project as requested.
    if args.initialize_project:
        if not args.project_name:
            print("Project name is required.")
            sys.exit(EXIT_USAGE)

        initialize_project(args.project_name, path=args.project_home, status=args.status)
        sys.exit(EXIT_OK)

    # Handle project by name requests.
    if args.project_name:
        project = autoload_project(args.project_name, include_disk=args.include_disk, path=args.project_home)

        if not project.is_loaded:
            print("Could not autoload the project: %s" % args.project_name)

            if project.has_error:
                print("Error: %s" % project.get_error())

            sys.exit(EXIT_OTHER)

        print(project.to_markdown())

        sys.exit(EXIT_OK)

    # Get the available types.
    project_types = get_project_types(args.project_home)

    # List the clients as requested.
    if args.client_code == "?":
        print("Available Client Codes")
        print("-" * 80)

        for c in get_project_clients(args.project_home):
            print(c)

        sys.exit(EXIT_OK)

    # List the status as requested.
    if args.status == "?":
        print("Available Status Codes")
        print("-" * 80)

        status_list = get_project_statuses(args.project_home)
        for s in status_list:
            print(s)

        sys.exit(EXIT_OK)

    # List the types as requested.
    if args.project_type == "?":
        print("Available Project Types")
        print("-" * 80)

        for t in project_types:
            print(t)

        sys.exit(EXIT_OK)

    # Print the report heading.
    heading = "Projects"
    if args.project_type:
        heading += "(%s)" % args.project_type

    print("=" * 105)
    print(heading)
    print("=" * 105)

    # Print the column headings.
    if args.project_type:
        print("%-40s %-10s %-11s %-15s %-5s %-4s" % ("Title", "Client", "Version", "Status", "Disk", "SCM"))
    else:
        print(
            "%-40s %-10s %-10s %-10s %-15s %-10s %-4s"
            % ("Title", "Type", "Client", "Version", "Status", "Disk", "SCM")
        )

    print("-" * 105)

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
        print("")
        print("No results.")
        sys.exit(EXIT_OK)

    dirty_count = 0
    error_count = 0
    for p in projects:

        if len(p.title) > 40:
            title = p.title[:37] + "..."
        else:
            title = p.title

        if p.config_exists:
            config_exists = ""
        else:
            config_exists = "*"

        if p.has_error:
            config_exists += " (e)"
            error_count += 1
        else:
            pass

        if p.is_dirty:
            dirty_count += 1
            scm = "%s+" % p.scm
        else:
            scm = p.scm

        if args.project_type:
            print(
                "%-40s %-10s %-10s %-15s %-5s %-4s %-1s"
                % (title, p.org, p.version, p.status, p.disk, p.scm, config_exists)
            )
        else:
            print(
                "%-40s %-10s %-10s %-10s %-15s %-10s %-4s %-1s"
                % (title, p.type, p.org, p.version, p.status, p.disk, scm, config_exists)
            )

    if len(projects) == 1:
        label = "result"
    else:
        label = "results"

    print("-" * 105)
    print("")
    print("%s %s." % (len(projects), label))

    if args.show_all:
        print("* indicates absence of project.ini file.")

    if error_count >= 1:
        print("(e) indicates an error parsing the project.ini file. Use the --name switch to find out more.")

    if dirty_count == 1:
        print("One project with uncommitted changes.")
    elif dirty_count > 1:
        print("%s projects with uncommitted changes." % dirty_count)
    else:
        print("No projects with uncommitted changes.")

    # Quit.
    sys.exit(EXIT_OK)


def version_update():
    """Increment the version number immediately after checking out a release branch."""

    __date__ = "2016-11-28"
    __help__ = """
#### When to Use

Generally, you want to increment the version number immediately after checking
out a release branch. However, you may wish to bump the version any time
during development, especially during early development where the MINOR
and PATCH versions are changing frequently.

Here is an example workflow:

    # Get the current version and check out the next release.
    versionbump myproject; # get the current version, example 1.2
    git checkout -b release-1.3;

    # Bump automatically sets the next minor version with a status of d.
    versionbump myproject -m -s d;

    # Commit the bump.
    git commit -am "Version Bump";

    # Go do the final work for the release.
    # ...

    # Merge the release.
    git checkout master;
    git merge --no-ff release-1.3;
    git tag -a 1.3;

    # Merge back to development.
    git checkout development;
    git merge --no-ff release-1.3;

#### Semantic Versioning

This utility makes use of [Semantic Versioning](semver.org). From the
documentation:

1. MAJOR version when you make incompatible API changes,
2. MINOR version when you add functionality in a backwards-compatible manner,
   and
3. PATCH version when you make backwards-compatible bug fixes.

Additional labels for pre-release and build metadata are available as
extensions to the MAJOR.MINOR.PATCH format.

**Status**

We define the following status codes:

- x Prototype, experimental. Use at your own risk.
- d Development. Unstable, untested.
- a Feature complete.
- b Ready for testing and QA.
- r Release candidate.
- o Obsolete, deprecated, or defect. End of life.

You may of course use whatever status you like.

#### Release Versus Version

**Release**

A *release* is a collection of updates representing a new version of the
product. A release is represented by the full string of MAJOR.MINOR.PATCH,
and may optionally include the status and build until the release is live.

The release is probably never displayed to Customers or Users.

**Version**

A *version* represents a specific state of the product. The version is
represented by the MAJOR.MINOR string of the release.

The version may be shown to Customers or Users.

    """
    __version__ = "0.11.1-d"

    # Define options and arguments.
    parser = ArgumentParser(description=__doc__, epilog=__help__, formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument(
        "project_name",
        help="The name of the project. Typically, the directory name in which the project is stored."
    )

    parser.add_argument(
        "-b=",
        "--build=",
        dest="build",
        help="Supply build meta data."
    )

    parser.add_argument(
        "-M",
        "--major",
        action="store_true",
        dest="major",
        help="Increase the major version number when you make changes to the public API that are "
             "backward-incompatible."
    )

    parser.add_argument(
        "-m",
        "--minor",
        action="store_true",
        dest="minor",
        help="Increase the minor version number when new or updated functionality has been implemented "
             "that does not change the public API."
    )

    parser.add_argument(
        "-n=",
        "--name=",
        dest="name",
        help="Name your release."
    )

    parser.add_argument(
        "-p",
        "--patch",
        action="store_true",
        dest="patch",
        help="Set (or increase) the patch level when backward-compatible bug-fixes have been implemented."
    )

    parser.add_argument(
        "-P=",
        "--path=",
        default=PROJECT_HOME,
        dest="path",
        help="The path to where projects are stored. Defaults to %s" % PROJECT_HOME
    )

    parser.add_argument(
        "--preview",
        action="store_true",
        dest="preview_only",
        help="Preview the output, but don't make any changes."
    )

    parser.add_argument(
        "-s=",
        "--status=",
        dest="status",
        help="Use the status to denote a pre-release version."
    )

    parser.add_argument(
        "-T=",
        "--template=",
        dest="template",
        help="Path to the version.py template you would like to use. Use ? to see the default."
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

    # This will display help or input errors as needed.
    args = parser.parse_args()
    # print args

    # Display the default version.py template.
    if args.template == "?":
        print(Version.get_template())
        sys.exit(EXIT_OK)

    # Get the project. Make sure it exists.
    project = Project(args.project_name, args.path)
    if not project.exists:
        print("Project does not exist: %s" % project.name)
        sys.exit(EXIT_INPUT)

    # Initialize version instance.
    version = Version(project.version)

    # Update the version or (by default) display the current version.
    if args.major:
        version.bump(major=True, status=args.status, build=args.build)
    elif args.minor:
        version.bump(minor=True, status=args.status, build=args.build)
    elif args.patch:
        version.bump(patch=True, status=args.status, build=args.build)
    else:
        print(version)
        sys.exit(EXIT_OK)

    # Set the version name.
    if args.name:
        version.name = args.name

    # Write the VERSION.txt file.
    if args.preview_only:
        print("Write: %s" % project.version_txt)
        print(version.to_string())
        print("")
    else:
        write_file(project.version_txt, version.to_string())

    # Write the version.py file.
    if project.version_py:
        if args.template:
            content = parse_template(version.get_context(), args.template)
        else:
            content = parse_template(version.get_context(), Version.get_template())

        if args.preview_only:
            print("Write: %s" % project.version_py)
            print("-" * 80)
            print(content)
            print("-" * 80)
            print("")
        else:
            write_file(project.version_py, content)

    # Quit.
    print(version.to_string())
    sys.exit(EXIT_OK)
