#! /usr/bin/env python

# Imports

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import commands
from ConfigParser import RawConfigParser
import os
import sys

# Administrivia

__author__ = "Shawn Davis <shawn@ptltd.co>"
__command__ = os.path.basename(sys.argv[0])
__date__ = "2016-10-30"
__version__ = "0.8.0-d"

# Constants

ENVIRONMENTS = ("base", "control", "development", "testing", "staging", "live")

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_INPUT = 2
EXIT_ENV = 3
EXIT_OTHER = 4

HELP = """
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

PROJECT_HOME = os.environ.get("PROJECT_HOME", "~/Work")

# Functions


def main():
    """List and filter projects in the projects directory."""

    description = main.__doc__

    # Define options and arguments.
    parser = ArgumentParser(description=description, epilog=HELP, formatter_class=RawDescriptionHelpFormatter)

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

    # This will display help or input errors as needed.
    args = parser.parse_args()
    # print args

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
        print "%-40s %-10s %-10s %-10s %-11s %-10s %-4s" % ("Title", "Type", "Client", "Version", "Status", "Disk", "SCM")

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


def autoload_project(name, include_disk=False, path="./"):
    """Attempt to automatically load the project configuration based on the name and path.

    :param name: The project name, or possible name.
    :type name: str

    :param include_disk: Whether to calculate disk space.
    :type include_disk: bool

    :param path: The base path to search.
    :type path: str

    :rtype: Project
    :returns: A ``Project`` instance or ``None`` if the project could not be found.

    """
    name = name.lower()
    names = (
        name,

        name.replace(".", "_"),
        name.replace(" ", "-"),
        name.replace(" ", "_"),
    )

    for name in names:
        root_path = os.path.join(path, name)
        if os.path.exists(root_path):
            project = Project(name, root_path)
            project.load(include_disk=include_disk)
            return project

    return None


def get_packages(ini, env):
    """Get packages for a given environment.

    :param ini: The configuration to scan.
    :type ini: str

    :param env: The environment name.
    :type env: str

    :rtype: list
    :returns: A list of ``Package`` instances.

    """

    a = list()
    for section in ini.sections():
        params = dict()

        for key, value in ini.items(section):
            params[key] = value

        package = Package(section, **params)

        if env in package.env:
            a.append(package)

    return a


def get_projects(path, criteria=None, include_disk=False, show_all=False):
    """Get a list of projects.

    :param path: Path to where projects are stored.
    :type path: str

    :param criteria: Criteria used to filter the list, if any.
    :type criteria: dict

    :param include_disk: Whether to calculate disk space used by the project.
    :type include_disk: bool

    :param show_all: By default, projects without a ``project.ini`` file are omitted. Set this to ``True`` to show all
                     projects.

    :type show_all: bool

    :rtype: list

    """
    names = list()
    projects = list()

    entries = os.listdir(path)

    for project_name in entries:

        # Get the project root path.
        project_root = os.path.join(path, project_name)

        # Projects are always stored as sub directories of path.
        if not os.path.isdir(project_root):
            continue

        # Skip projects we've already found.
        if project_name in names:
            continue

        # Load the project.
        project = Project(project_name, project_root)
        project.load(include_disk=include_disk)
        # print(project)

        # We skip the display of the project if a project config does not exist and show_all is False.
        if not project.config_exists and not show_all:
            continue

        # Filter based on criteria, which should be a dict.
        if criteria:
            for field, search in criteria.items():
                value = getattr(project, field)
                if search == value:
                    projects.append(project)
        else:
            projects.append(project)

    return projects


def get_project_clients(path):
    clients = list()

    projects = get_projects(path)
    for p in projects:
        if p.org not in clients:
            clients.append(p.org)

    return sorted(clients)


def get_project_statuses(path):
    statuses = list()

    projects = get_projects(path)
    for p in projects:
        if p.status not in statuses:
            statuses.append(p.status)

    return sorted(statuses)


def get_project_types(path):
    types = list()

    projects = get_projects(path)
    for p in projects:
        if p.type not in types:
            types.append(p.type)

    return sorted(types)


class Section(object):

    def __init__(self, key, **kwargs):
        self._context = kwargs
        self._name = key

    def __getattr__(self, item):
        return self._context[item]

    def get_context(self):
        """Return the section as a dictionary.

        :rtype: dict

        """
        return self._context.copy()

    def to_markdown(self):
        """Convert the section to Markdown.

        :rtype: str

        """
        a = list()
        a.append("## %s" % self._name.title())
        a.append("")

        context = self.get_context()

        if "description" in context:
            a.append(context.pop("description"))
            a.append("")

        for key, value in context.items():
            if key == "tags":
                a.append("*tags*: %s  " % ",".join(value))
            else:
                a.append("*%s*: %s  " % (key, value))

        a.append("")

        return "\n".join(a)


class Package(object):
    """A package to be included in a requirements file.

    .. code-block:: ini

        [django]
        cmd = django==1.9.9
        docs = http://docs.djangoproject.com
        env = base
        home = http://djangoproject.com
        note = We use this all the time.
        scm = http://github.com/django/django
        title = Django

    """

    def __init__(self, name, **kwargs):
        self.cmd = kwargs.get("cmd", None)
        self.docs = kwargs.get("docs", None)
        self.env = kwargs.get("env", "base")
        self.home = kwargs.get("home", None)
        self.name = name
        self.note = kwargs.get("note", None)
        self.scm = kwargs.get("scm", None)
        self.title = kwargs.get("title", name)

    @property
    def has_links(self):
        if self.docs:
            return True
        elif self.home:
            return True
        elif self.scm:
            return True
        else:
            return False

    def to_markdown(self):
        a = list()

        a.append("**%s**" % self.title)
        a.append("")

        if self.note:
            a.append(self.note)
            a.append("")

        a.append("Part of the *%s* environment." % self.env)
        a.append("")

        # Example: [Link text](http://example.com/>)
        if self.has_links:
            a.append("Links:")
            a.append("")

            if self.home:
                a.append("- [Home](%s)" % self.home)

            if self.docs:
                a.append("- [Documentation](%s)" % self.docs)

            if self.scm:
                a.append("- [Source](%s)" % self.scm)

            a.append("")

        if self.cmd:
            a.append("To install manually:")
            a.append("")
            a.append("    pip install %s" % self.cmd)

        a.append("")
        return "\n".join(a)

    def to_rst(self):
        a = list()

        a.append(self.title)
        a.append("-" * len(self.title))
        a.append("")

        if self.note:
            a.append(self.note)
            a.append("")

        a.append("Part of the *%s* environment." % self.env)
        a.append("")

        # Example: `Link text <http://example.com/>`_
        if self.has_links:
            if self.home:
                a.append("- `Home <%s/>`_" % self.home)

            if self.docs:
                a.append("- `Documentation <%s/>`_" % self.docs)

            if self.scm:
                a.append("- `Source <%s/>`_" % self.scm)

            a.append("")

        a.append("To install manually:")
        a.append("")
        a.append(".. code-block:: bash")
        a.append("")

        if self.cmd:
            a.append("    pip install %s" % self.cmd)
        else:
            a.append("    pip install %s" % self.name)

        a.append("")
        return "\n".join(a)


class Project(object):

    def __init__(self, name, path, debug=False):
        """Initialize a project object.

        :param name: The name of the project.
        :type name: str

        :param path: The path to the project.
        :type path: str

        :param debug: Enable debug mode. Only useful in development.
        :type debug: bool

        """
        self.config_exists = None
        self.config_path = None
        self.debug = debug
        self.description = None
        self.disk = "TBD"
        self.is_dirty = None
        self.is_loaded = False
        self.name = name
        self.org = "Unknown"
        self.root = path
        self.scm = None
        self.status = "unknown"
        self.tags = list()
        self.title = None
        self.type = "project"
        self.version = "0.1.0-d"
        self._requirements = list()
        self._sections = list()

        config_path = os.path.join(path, "project.ini")
        if os.path.exists(config_path):
            self.config_exists = True
            self.config_path = config_path
        else:
            self.config_exists = False

    def __str__(self):
        return self.title or self.name or "Untitled Project"

    def get_context(self):
        """Get project data as a dictionary.

        :rtype: dict

        """
        d = {
            'config_exists': self.config_exists,
            'description': self.description,
            'disk': self.disk,
            'name': self.name,
            'org': self.org,
            'root': self.root,
            'scm': self.scm,
            'status': self.status,
            'title': self.title,
            'type': self.type,
            'version': self.version,
        }

        for section_name in self._sections:
            d[section_name] = getattr(self, section_name)

        return d

    def load(self, include_disk=False):
        return self._load(self.root, include_disk=include_disk)

    def to_markdown(self):
        """Output the project as Markdown.

        :rtype: str

        """
        # TODO: Create a TEMPLATE for markdown export and make this configurable from a switch.

        # Build the top/main section of the output.
        a = list()
        a.append("# %s" % self.title)
        a.append("")

        a.append("**Version**: %s  " % self.version)
        a.append("**Status**: %s  " % self.status)
        a.append("**Type**: %s  " % self.type)
        a.append("**Disk Usage**: %s  " % self._get_disk())
        a.append("**Source Code Management**: %s  " % self._get_scm())

        if self.tags:
            a.append("**Tags**: %s" % ",".join(self.tags))

        a.append("")

        # Add the description.
        if self.description:
            a.append(self.description)
            a.append("")

        # Add each section to the output.
        context = self.get_context()
        for key, value in context.items():
            if isinstance(value, Section):
                a.append(value.to_markdown())
            else:
                pass

        # List the dependencies.
        deps = self._get_dependencies()
        if deps:
            a.append("## Dependencies")
            a.append("")

            for env, packages in deps:

                if len(packages) == 0:
                    continue

                a.append("### %s" % env)
                a.append("")

                for p in packages:
                    a.append(p.to_markdown())

        # Include the project tree.
        a.append("## Tree")
        a.append("")
        status, output = commands.getstatusoutput("tree %s" % self.root)
        for line in output.split("\n"):
            a.append("    %s" % line)

        a.append("")

        return "\n".join(a)

    def _file_exists(self, name):
        if not self.root:
            raise ValueError("project root must be defined")

        path = os.path.join(self.root, name)
        return os.path.exists(path)

    def _get_dependencies(self):
        """Get project dependencies from a ``packages.ini`` file.

        :rtype list
        :returns: A list of ``(env, packages)``.
        """
        # TODO: Add public documentation for project dependencies.
        locations = (
            os.path.join("deploy", "requirements", "packages.ini"),
            os.path.join("requirements/packages.ini"),
            os.path.join("requirements.ini"),
        )

        a = list()
        for i in locations:
            if self._file_exists(i):
                path = os.path.join(self.root, i)

                ini = RawConfigParser()
                ini.read(path)

                for env in ENVIRONMENTS:
                    a.append((env, get_packages(ini, env)))

        return a

    def _get_disk(self):
        cmd = "du -hs %s | awk -F ' ' '{print $1}'" % self.root
        (status, output) = commands.getstatusoutput(cmd)
        return output.strip()

    def _get_org(self):
        obj = getattr(self, "client", None)
        if obj:
            try:
                return obj.code
            except AttributeError:
                return "Unidentified"

        obj = getattr(self, "business", None)
        if obj:
            try:
                return obj.code
            except AttributeError:
                return "Internal"

        return "Unknown"

    def _get_path(self, name):
        return os.path.join(self.root, name)

    def _get_scm(self):
        """Determine the SCM in use and get the current state."""
        if self._file_exists(".git"):
            # See http://stackoverflow.com/a/5737794/241720
            cmd = '(cd %s && test -z "$(git status --porcelain)")' % self.root
            (status, output) = commands.getstatusoutput(cmd)
            if status >= 1:
                self.is_dirty = True
            else:
                self.is_dirty = False

            return "git"
        elif self._file_exists(".hg"):
            # TODO: Determine if hg repo is dirty.
            return "hg"
        elif self._file_exists("trunk"):
            # TODO: Determine if svn repo is dirty.
            return "svn"
        else:
            return "None"

    def _get_version(self):
        if self._file_exists("VERSION.txt"):
            with open(self._get_path("VERSION.txt"), "rb") as f:
                v = f.read().strip()
                f.close()
                return v
        else:
            return "0.1.0-d"

    def _load(self, path, include_disk=False):
        """Attempt to load a project configuration from a given path.

        :param path: Path to the project.
        :type path: str

        :param include_disk: Whether to calculate disk usage.
        :type include_disk: bool

        :rtype: bool
        :returns: Returns ``True`` if the project was found and loaded successful. This also sets ``is_loaded`` to
                  ``True``.

        """

        # We can't do anything if the project root doesn't exist.
        if not os.path.exists(self.root):
            return False

        # Load the configuration.
        if self.config_exists:

            # Load the config without interpolation.
            ini = RawConfigParser()
            ini.read(self.config_path)

            # Iterate through the sections.
            for section_name in ini.sections():

                if self.debug:
                    print "[%s]" % section_name

                kwargs = {}

                for key, value in ini.items(section_name):
                    if key == "tags":
                        kwargs['tags'] = value.split(",")
                    else:
                        kwargs[key] = value

                if section_name == "project":
                    for key in kwargs.keys():
                        setattr(self, key, kwargs[key])
                else:
                    section = Section(section_name, **kwargs)
                    self._sections.append(section_name)
                    setattr(self, section_name, section)

        # Make sure we always have title.
        if not self.title:
            self.title = self.name

        # Get meta data.
        self.org = self._get_org()
        self.scm = self._get_scm().strip()
        self.version = self._get_version()

        # Calculate disk space.
        if include_disk:
            self.disk = self._get_disk()

        # Set loaded status.
        self.is_loaded = True
        return True

# Kickoff
if __name__ == "__main__":
    main()