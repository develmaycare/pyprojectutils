# Imports

from collections import OrderedDict
import os
from colors import cyan, green, red, yellow
from .config import Config, Section
from .constants import BITBUCKET_USER, DEVELOPER_CODE, DEVELOPER_NAME, ENVIRONMENTS, GITHUB_USER, LINK_CATEGORIES, PROJECT_ARCHIVE, PROJECT_HOME, \
    PROJECTS_ON_HOLD
from .links import Link
from .organizations import Business, Client
from .packaging import PackageConfig
from .repos import Repo
from .shell import Command
from .shortcuts import bool_to_yes_no, find_file, parse_template, read_file, write_file, print_info

# Constants

GITIGNORE_TEMPLATE = """*.pyc
.DS_Store
.idea
tmp.*
tmp
"""

PROJECT_INI_TEMPLATE = """[project]
category = $category
description = $description
status = $status
title = $title
type = $type

[business]
code = $business_code
name = $business_name

[client]
code = $client_code
name = $client_name

[domain]
name = example
tld = com

"""

README_TEMPLATE = """# $title

$description

"""

# Exports

__all__ = (
    "autoload_project",
    "get_projects",
    "initialize_project",
    "Project",
)

# Functions


def autoload_project(name, include_cloc=False, include_disk=False, path=None):
    """Attempt to automatically load the project configuration based on the name and path.

    :param name: The project name, or possible name.
    :type name: str

    :param include_cloc: Whether to include information on lines of code.
    :type include_cloc: bool

    :param include_disk: Whether to calculate disk space.
    :type include_disk: bool

    :param path: The path where projects are located.
    :type path: str

    :rtype: Project
    :returns: ``is_loaded`` will be ``True`` on the ``Project`` instance if the project was found.

    .. versionchanged:: 0.27.0-d
        In versions prior to this one, autoload only looked for the project on the given path or in ``PROJECT_HOME`` if
        no path was given. Now, an attempt will also be made to find the project in ``PROJECTS_ON_HOLD`` and
        ``PROJECT_ARCHIVE`` (in that order).

        ``include_cloc`` was also added in support of the ``statproject`` command.

    """
    # Automatically handle different names for the project.
    name = name.lower()
    names = (
        name,
        name.replace(".", "_"),
        name.replace(" ", "-"),
        name.replace(" ", "_"),
    )

    # Find the project on the given path or in PROJECT_HOME using the provided names.
    for name in names:
        root_path = os.path.join(path or PROJECT_HOME, name)
        if os.path.exists(root_path):
            project = Project(root_path)
            project.load(include_cloc=include_cloc, include_disk=include_disk)
            return project

    # If the project is not found above attempt to find it in PROJECTS_ON_HOLD.
    for name in names:
        root_path = os.path.join(PROJECTS_ON_HOLD, name)
        if os.path.exists(root_path):
            project = Project(root_path)
            project.load(include_cloc=include_cloc, include_disk=include_disk)
            return project

    # Last, looking the PROJECT_ARCHIVE.
    for name in names:
        root_path = os.path.join(PROJECT_ARCHIVE, name)
        if os.path.exists(root_path):
            project = Project(root_path)
            project.load(include_cloc=include_cloc, include_disk=include_disk)
            return project

    # If no project is found, we will still return a project instance.
    return Project(name)


def find_current_project():
    """Find the project based on the current working directory.

    :rtype: Project || None

    .. versionadded:: 0.27.2-d

    """
    # We'll attempt to determine the current project based on the current working directory.
    files = (
        "project.ini",
        "VERSION.txt",
        "DESCRIPTION.txt",
    )
    for f in files:
        file_path = find_file(f, os.getcwd())

        if file_path:
            project_name = os.path.basename(os.path.dirname(file_path))
            project_home = os.path.dirname(os.path.dirname(file_path))
            print("autoload_project(%s, path=%s)" % (project_name, project_home))
            return autoload_project(project_name, path=project_home)

    return None


def find_project(name, path=None):
    """Find a project using by name, regardless of where the user is in the current directory structure.

    :param name: The name of the project.
    :type name: str

    :param path: The path to search. By default, ``PROJECT_HOME``, ``PROJECTS_ON_HOLD``, and ``PROJECT_ARCHIVE`` are
                 searched (in that order).
    :type path: str

    :rtype: Project
    :returns: A ``Project`` instance or ``None`` if the project could not be found.

    .. versionadded:: 0.27.2-d

    """
    # If a path is given, we will only look for the project on that path. Otherwise, let autload_project() do it's
    # thing.
    if path:
        return autoload_project(name, path=path)
    else:
        return autoload_project(name)


def get_clients(path):
    d = dict()
    projects = get_projects(path)

    for p in projects:
        client = p.get_client()

        if client.code in d.keys():
            d[client.code].projects.append(p)
        else:
            client.projects.append(p)
            d[client.code] = client

    return OrderedDict(sorted(d.items(), key=lambda t: t[0]))


def get_distinct_project_attributes(attribute, path=PROJECT_HOME):
    """Get distinct values of the named attribute.

    .. versionadded:: 0.16.0-d

    :param attribute: The name of the attribute.
    :type attribute: str

    :param path: The path to where projects are stored.
    :type path: str

    :rtype: OrderedDict
    :returns: Returns a dictionary where each distinct values is a dictionary key and the total project count is the
              dictionary value. Keys are sorted alphabetically.

    .. note::
        If the given ``attribute`` does not exist on the :py:class:`Project`, the resulting ``AttributeError`` is
        trapped and ``{'Invalid Project Attribute': attribute}`` is returned.

    """
    d = dict()
    projects = get_projects(path)
    for p in projects:
        try:
            value = getattr(p, attribute)
        except AttributeError:
            return {'Invalid Project Attribute': attribute}

        if value in d.keys():
            d[value] += 1
        else:
            d[value] = 1

    return OrderedDict(sorted(d.items(), key=lambda t: t[0]))


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

    .. versionchanged:: 0.16.0-d
        When filtering criteria includes ``name`` or ``description``, these are handled using partial rather than full
        matching. The matching is also case insensitive.

    .. versionchanged:: 0.27.0-d
        Updated for new signature of :py:class:`Project` init.

    """
    names = list()
    projects = list()

    entries = os.listdir(path)

    for project_name in entries:

        # Get the project root path.
        root_path = os.path.join(path, project_name)

        # Projects are always stored as sub directories of path.
        if not os.path.isdir(root_path):
            continue

        # Ignore dot directories.
        if project_name[0] == ".":
            continue

        # Skip projects we've already found.
        if project_name in names:
            continue

        # Load the project.
        project = Project(root_path)
        project.load(include_disk=include_disk)
        # print(project)

        # We skip the display of the project if a project config does not exist and show_all is False.
        if not project.config_exists and not show_all:
            continue

        # Filter based on criteria, which should be a dict.
        if criteria:
            for field, search in criteria.items():

                # Handle the name and description attributes differently.
                if field in ("description", "name"):
                    value = getattr(project, field).lower()
                    search = search.lower()
                    if search in value:
                        projects.append(project)
                elif field == "tag":
                    tags = getattr(project, "tags")
                    if search in tags:
                        projects.append(project)
                else:
                    value = getattr(project, field)
                    if search == value:
                        projects.append(project)
        else:
            projects.append(project)

    return projects


def format_projects_for_csv(projects, include_columns=True):
    """Get the project list for output as CSV.

    :param projects: The project list as returned by ``get_projects()``.
    :type projects: list[Project]

    :param include_columns: Include column headings.
    :type include_columns: bool

    :rtype: str

    """

    count = 0
    output = list()
    for p in projects:
        if count == 0:
            if include_columns:
                output.append(p.to_csv(include_header=True))
            else:
                output.append(p.to_csv())

            continue

        count += 1
        output.append(p.to_csv())

    return "\n".join(output)


def format_projects_for_html(projects, css_classes="table table-bordered table-striped", color_enabled=False,
                             heading="Projects", include_columns=True, links_enabled=False, show_branch=False,
                             wrapped=False):
    """Get the project list for output as HTML.

    :param projects: The project list as returned by ``get_projects()``.
    :type projects: list[Project]

    :param css_classes: The CSS classes to apply to the table.
    :type css_classes: str

    :param color_enabled: Enable output coloring.
    :type color_enabled: bool

    :param heading: The heading appears before other output when ``wrap`` is ``True``.
    :type heading: str

    :param include_columns: Include column headings.
    :type include_columns: bool

    :param links_enabled: Transform the title into a link. The linking strategy uses the first file it finds, either:
                          ``docs/build/html/index.html`` or ``README.html``. Failing that, it uses
                          ``file://project_root``.
                          All links are created with ``target="_blank"``.
    :type links_enabled: bool

    :param show_branch: Show SCM branch.
    :type show_branch: bool

    :param wrapped: Wrap the output in a basic HTML template (based on Twitter Bootstrap).
    :type wrapped: bool

    :rtype: str

    .. versionchanged:: 0.27.3-d
        Added support for additional links related to the project.

    """
    output = list()

    if wrapped:
        output.append('<html>')
        output.append('<head>')
        output.append(
            '<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">'
        )
        output.append(
            '<link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">'
        )
        output.append('</head>')
        output.append('<body>')
        output.append('<div class="container">')
        output.append('<h2>%s</h2>' % heading)

    # If there are no projects, just say so.
    if len(projects) == 0:
        output.append('<p>No results.</p>')

        if wrapped:
            output.append('</div>')
            output.append('</body>')
            output.append('</html>')

        return "\n".join(output)

    # Create the header.
    if css_classes:
        output.append('<table class="%s">' % css_classes)
    else:
        output.append('<table>')

    if include_columns:
        output.append('<thead>')
        output.append('<tr>')

        for column in ("Title", "Description", "Category", "Type", "Org", "Version", "Status", "Disk", "SCM", "Tools"):
            output.append('<th>%s</th>' % column)

        output.append('</tr>')
        output.append('</thead>')

    # Create the table.
    output.append('<tbody>')
    dirty_count = 0
    dirty_list = list()
    error_count = 0
    for p in projects:

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
            dirty_list.append(p.name)
            scm = "%s+" % p.scm
        else:
            scm = str(p.scm)

        if show_branch:
            if p.branch:
                scm += " (%s)" % p.branch
            else:
                scm += " (unknown)"

        if color_enabled:
            if p.has_error:
                output.append('<tr class="danger">')
            elif p.is_dirty:
                output.append('<tr class="warning">')
            elif p.status == "live":
                output.append('<tr class="success">')
            elif p.status == "unknown":
                output.append('<tr class="info">')
            else:
                output.append('<tr>')
        else:
            output.append('<tr>')

        if links_enabled:
            if p.path_exists("docs/build/html/index.html"):
                url = os.path.join(p.root, "docs/build/html/index.html")
            elif p.path_exists("README.html"):
                url = os.path.join(p.root, "README.html")
            # elif p.has_section("urls") and p.urls.has_attribute("project"):
            #     url = p.urls.project.url
            else:
                url = p.root

            link = '<a href="%s" target="_blank">%s</a>' % (url, p.title)

            output.append('<td>%s</td>' % link)
        else:
            output.append('<td>%s</td>' % p.title)

        output.append('<td>%s</td>' % p.description)
        output.append('<td>%s</td>' % p.category)
        output.append('<td>%s</td>' % p.type)
        output.append('<td>%s</td>' % p.org)
        output.append('<td>%s</td>' % p.version)
        output.append('<td>%s</td>' % p.status)
        output.append('<td>%s</td>' % p.disk)
        output.append('<td>%s</td>' % scm)

        if links_enabled:
            if p.has_section("urls"):
                links = list()

                if config_exists:
                    links.append(config_exists)

                for link in p.urls.get_links():
                    links.append(link.to_html())

                output.append('<td>%s</td>' % "&nbsp; ".join(links))

            else:
                output.append('<td>%s</td>' % config_exists)
        else:
            output.append('<td>%s</td>' % config_exists)

        output.append('</tr>')

    # Close the table.
    output.append('<tfoot>')
    output.append('<tr>')
    output.append('<td></td>')
    output.append('<td></td>')
    output.append('<td></td>')
    output.append('<td></td>')
    output.append('<td></td>')
    output.append('<td></td>')
    output.append('<td></td>')
    output.append('<td></td>')
    output.append('<td>%s dirty</td>' % dirty_count)
    output.append('<td>%s error(s)</td>' % error_count)
    output.append('</tr>')
    output.append('</tfoot>')
    output.append('</tbody>')
    output.append('</table>')

    if wrapped:
        output.append('</div>')
        output.append('</body>')
        output.append('</html>')

    return "\n".join(output)


def format_projects_for_shell(projects, color_enabled=False, heading="Projects", show_all=False, show_branch=False):
    """Get project list for output to shell.

    :param projects: The project list as returned by ``get_projects()``.
    :type projects: list[Project]

    :param color_enabled: Enable output coloring.
    :type color_enabled: bool

    :param heading: The heading label that appears at the top of the output.
    :type heading: str

    :param show_all: Indicates show all projects was requested.
    :type show_all: bool

    :param show_branch: Show SCM branch.
    :type show_branch: bool

    :rtype: str

    .. versionadded: 0.27.0-d

    """
    output = list()

    output.append("=" * 130)
    output.append(heading)
    output.append("=" * 130)

    # Print the column headings.
    output.append(
        "%-30s %-20s %-15s %-5s %-10s %-15s %-10s %-20s"
        % ("Title", "Category", "Type", "Org", "Version", "Status", "Disk", "SCM")
    )
    output.append("-" * 130)

    # Print the rows.
    if len(projects) == 0:
        output.append("")
        output.append("No results.")
        return "\n".join(output)

    dirty_count = 0
    dirty_list = list()
    error_count = 0
    for p in projects:

        if len(p.title) > 30:
            title = p.title[:27] + "..."
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
            dirty_list.append(p.name)
            scm = "%s+" % p.scm
        else:
            scm = str(p.scm)

        if show_branch:
            if p.branch:
                scm += " (%s)" % p.branch
            else:
                scm += " (unknown)"

        line = "%-30s %-20s %-15s %-5s %-10s %-15s %-10s %-4s %-1s" % (
            title,
            p.category,
            p.type,
            p.org,
            p.version,
            p.status,
            p.disk,
            scm,
            config_exists
        )

        if color_enabled:
            if p.has_error:
                output.append(red(line))
            elif p.is_dirty:
                output.append(yellow(line))
            elif p.status == "live":
                output.append(green(line))
            elif p.status == "unknown":
                output.append(cyan(line))
            else:
                output.append(line)
        else:
            output.append(line)

    if len(projects) == 1:
        label = "result"
    else:
        label = "results"

    output.append("-" * 130)
    output.append("")
    output.append("%s %s." % (len(projects), label))

    if show_all:
        output.append("* indicates absence of project.ini file.")

    if error_count >= 1:
        output.append("(e) indicates an error parsing the project.ini file. Use the --name switch to find out more.")

    if dirty_count == 1:
        output.append("One project with uncommitted changes: %s" % dirty_list[0])
    elif dirty_count > 1:
        output.append("%s projects with uncommitted changes." % dirty_count)
        output.append("")

        for i in dirty_list:
            output.append("    cd %s/%s && git st" % (PROJECT_HOME, i))

        output.append("")
    else:
        output.append("No projects with uncommitted changes.")

    return "\n".join(output)

# Classes


class Project(Config):

    def __init__(self, path):
        """Initialize a project object.

        :param path: The path to the project.
        :type path: str

        .. versionchanged:: 0.27.0-d
            The ``name`` parameter was removed. It is now derived from the base name of the ``path``.

        """
        self.branch = None
        self.business = None
        self.category = None or "uncategorized"
        self.client = None
        self.config_exists = None
        self.description = None
        self.description_exists = None
        self.disk = "TBD"
        self.gitignore_exists = None
        self.is_dirty = None
        self.is_loaded = False
        self.languages = dict()
        self.license = None
        self.license_exists = None
        self.makefile_exists = None
        self.manifest_exists = None
        self.name = os.path.basename(path)
        self.org = "Unknown"
        self.readme_exists = None
        self.requirements_exists = None
        self.root = path
        self.scm = None
        self.setup_exists = None
        self.status = "unknown"
        self.tags = list()
        self.title = None
        self.total_directories = None
        self.total_files = None
        self.type = "project"
        self.version = "0.1.0-d"
        self.version_exists = None
        self._requirements = list()

        # Set the default slug. This may be overridden if a title is available during load().
        self.slug = self.name

        # Handle config file. We have to do this here in order to call super() below.
        config_path = os.path.join(self.root, "project.ini")
        if os.path.exists(config_path):
            self.config_exists = True
        else:
            self.config_exists = False

        super(Project, self).__init__(config_path)

    def __str__(self):
        return self.name

    @property
    def exists(self):
        """Indicates whether the project root exists.

        :rtype: bool

        .. note::
            We've made this a dynamic property because it is possible for the root to be created after the project
            instance has been created.

        """
        return os.path.exists(self.root)

    def get_archive_path(self):
        """Get the path to where this project should be archived.

        :rtype: str
        :raises: ValueError

        .. note::
            This path does *no* include the project name.

        """
        if self.has_client:
            return os.path.join(PROJECT_ARCHIVE, "clients", self.client.code)
        elif self.has_business:
            return os.path.join(PROJECT_ARCHIVE, "business")
        else:
            raise ValueError("No business or client defined. It's not possible to derive a path. I can't work under "
                             "these conditions.")

    def get_business(self):
        """Get the project business instance.

        :rtype: Business

        .. note::
            This method exists because we don't always know if ``business`` has been populated. This allows us to return
            a default even if the client has not been defined.

        """
        if self.has_business:
            return self.business

        return Business(DEVELOPER_NAME, code=DEVELOPER_CODE)

    def get_client(self):
        """Get the project client instance.

        :rtype: Client

        .. note::
            This method exists because we don't always know if ``client`` has been populated. This allows us to return a
            default even if the client has not been defined.

        """
        if self.has_client:
            return self.client

        return Client("Unidentified", code="UNK")

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

    def get_repo(self):
        """Get repo information for the project.

        :rtype: repos.Repo

        .. versionadded:: 0.27.3-d

        """
        return Repo(self.name, cli=self.scm, project=self.title)

    def get_requirements(self, env=None, manager=None):
        """Get project requirements (dependencies).

        :param env: Filter by environment.
        :type env: str

        :param manager: Filter by package manager.
        :type manager: str

        :rtype: list[Section] || list[str]

        """
        locations = (
            os.path.join("deploy", "requirements", "packages.ini"),
            os.path.join("requirements/packages.ini"),
            os.path.join("requirements.ini"),
        )

        for i in locations:
            if self.path_exists(i):
                path = os.path.join(self.root, i)

                config = PackageConfig(path)
                if config.load():
                    return config.get_packages(env=env, manager=manager)

        # If we've gotten this far, there is not packages.ini file. So we'll attempt to return the contents of the
        # requirements.pip file if it exists.
        if self.path_exists("requirements.pip"):
            content = read_file(os.path.join(self.root, "requirements.pip"))
            return content.split("\n")

        return list()

    def get_tree(self):
        """Get the output of a tree command on the project.

        :rtype: str

        """
        command = Command("tree %s" % self.root)
        if command.run():
            output = command.output

            # Remove the first line which is the path.
            a = output.split("\n")
            a.pop(0)

            #  Also remove pyc files.
            b = list()
            for line in a:
                if ".pyc" in line:
                    continue

                b.append(line)

            return "\n".join(b)
        else:
            return "Not Available"

    @property
    def has_business(self):
        """Indicates whether the project has a business (developer).

        :rtype: bool

        """
        return self.business is not None

    @property
    def has_client(self):
        """Indicates whether the project has a client.

        :rtype: bool

        """
        return self.client is not None

    @property
    def has_packages_ini(self):
        """Indicates whether the projec has a ``packages.ini`` file.

        :rtype bool

        """
        locations = (
            os.path.join("deploy", "requirements", "packages.ini"),
            os.path.join("requirements/packages.ini"),
            os.path.join("requirements.ini"),
        )

        for i in locations:
            if self.path_exists(i):
                return True

        return False

    @property
    def has_scm(self):
        return self._get_scm() is not None

    def initialize(self, display=True):
        """Initialize the project, creating various meta files as needed.

        :param display: Display output or not.
        :type display: bool

        This method does the following:

        - Creates the project root if it does not exist.
        - Writes ``DESCRIPTION.txt`` if one does not exist and ``description`` is set.
        - Writes a starter ``.gitignore`` file if one does not exist.
        - Writes a default (and very bare) ``README.markdown`` file if one does not exist.
        - Creates an empty ``requirements.pip`` file if one does not exist.
        - Creates a ``LICENSE.txt`` file if one does not exist and ``license`` is set.
        - Writes a starter ``project.ini`` file if one does not exist.

        .. note::
            It is safe to run this method multiple times.

        .. versionadded:: 0.16.0-d

        """
        if not os.path.exists(self.root):
            if display:
                print_info("Creating project directory: %s" % self.root)

            os.makedirs(self.root)

        description_path = os.path.join(self.root, "DESCRIPTION.txt")
        if self.description and not os.path.exists(description_path):
            if display:
                print_info("Writing DESCRIPTION.txt file: %s" % description_path)

            write_file(description_path, self.description)

        gitignore_path = os.path.join(self.root, ".gitignore")
        if not os.path.exists(gitignore_path):
            if display:
                print_info("Creating .gitignore file: %s" % gitignore_path)

            write_file(gitignore_path, GITIGNORE_TEMPLATE)

        license_path = os.path.join(self.root, "LICENSE.txt")
        if self.license and not os.path.exists(license_path):
            print_info("Creating %s license file: %s" % (self.license, license_path))

            if self.has_client:
                org = self.client.name
            elif self.has_business:
                org = self.business.name
            else:
                org = DEVELOPER_NAME

            command = Command("lice --org=%s --proj=%s %s > %s" % (org, self.title, self.license, license_path))
            command.run()

        ini_path = os.path.join(self.root, "project.ini")
        if not os.path.exists(ini_path):
            print_info("Creating default project.ini file: %s" % ini_path)

            business = self.get_business()
            client = self.get_client()

            context = {
                'business_code': business.code,
                'business_name': business.name,
                'category': self.category,
                'client_code': client.code,
                'client_name': client.name,
                'description': self.description or "",
                'status': self.status or "development",
                'title': self.title or self.name,
                'type': self.type,
            }
            # print context

            content = parse_template(context, PROJECT_INI_TEMPLATE)
            write_file(ini_path, content)

        readme_path = os.path.join(self.root, "README.markdown")
        if not os.path.exists(readme_path):
            print_info("Writing default README.markdown file: %s" % readme_path)
            context = {
                'description': self.description or "",
                'title': self.title or self.name,
            }
            content = parse_template(context, README_TEMPLATE)
            write_file(readme_path, content)

        requirements_path = os.path.join(self.root, "requirements.pip")
        if not os.path.exists(requirements_path):
            print_info("Creating empty requirements file.")
            command = Command("touch %s" % requirements_path)
            command.run()

        version_path = os.path.join(self.root, "VERSION.txt")
        if not os.path.exists(version_path):
            print_info("Writing initial version file: %s" % version_path)
            write_file(version_path, self.version)

        return True

    # noinspection SpellCheckingInspection
    def load(self, include_cloc=False, include_disk=False):
        """Load the project.

        :param include_cloc: Whether to include information on lines of code.
        :type include_cloc: bool

        :param include_disk: Whether to calculate disk usage.
        :type include_disk: bool

        :rtype: bool
        :returns: Returns ``True`` if the project was found and loaded successful. This also sets ``is_loaded`` to
                  ``True``.

        .. versionchanged: 0.27.0-d
            Added checks for common meta files. Also added ``include_cloc`` parameter.

        """
        # We can't do anything if the project root doesn't exist.
        if not self.exists:
            self.is_loaded = False
            self._error = "Project root does not exist: %s" % self.root
            return False

        # Assemble context.
        context = {
            'ANSIBLE': "http://docs.ansible.com",
            'BITBUCKET': "https://bitbucket.org/%s/%s" % (BITBUCKET_USER, self.name),
            'BITBUCKET_ISSUES': "https://bitbucket.org/%s/%s/issues" % (BITBUCKET_USER, self.name),
            'BITBUCKET_USER': BITBUCKET_USER,
            'GITHUB': "https://github.com/%s/%s" % (GITHUB_USER, self.name),
            'GITHUB_ISSUES': "https://github.com/%s/%s/issues" % (GITHUB_USER, self.name),
            'GITHUB_USER': GITHUB_USER,
            'PROJECT_NAME': self.name,
            'WAFFLE': "https://waffle.io/%s/%s" % (GITHUB_USER, self.name),
            'WAFFLE_USER': GITHUB_USER,
        }

        # Let the underlying Config do it's thing.
        super(Project, self).load(context=context)

        # Make sure we always have title.
        if not self.title:
            self.title = self.name

        # Set the slug.
        self.slug = self.title.replace(" ", "-").lower()

        # Get meta data.
        self.org = self._get_org()
        self.scm = self._get_scm()
        self._load_version()

        # Calculate disk space.
        if include_disk:
            self.disk = self._get_disk()

        # Determine if various meta files exist.
        self.description_exists = self.path_exists("DESCRIPTION.txt")
        self.gitignore_exists = self.path_exists(".gitignore")
        self.license_exists = self.path_exists("LICENSE.txt")
        self.makefile_exists = self.path_exists("Makefile")
        self.manifest_exists = self.path_exists("MANIFEST.in")
        self.readme_exists = self.path_exists("README.markdown")
        self.requirements_exists = self.path_exists("requirements.pip")
        self.setup_exists = self.path_exists("setup.py")
        self.version_exists = self.path_exists("VERSION.txt")

        # Get the number of files and directories. 4 directories, 63 files
        command = Command("tree %s | tail -1" % self.root)
        if command.run():
            self.total_directories = command.output.split(", ")[0].split(" ")[0]
            self.total_files = command.output.split(", ")[1].split(" ")[0]

        # command = 'tree | tail -1 | awk -F "," ' + "'{print $1}' | " + 'awk -F " " ' + "'{print $1}'"
        # status, output = commands.getstatusoutput("cd %s && %s" % (self.root, command))
        # self.total_directories = output.strip()
        #
        # command = 'tree | tail -1 | awk -F "," ' + "'{print $2}' | " + 'awk -F " " ' + "'{print $1}'"
        # status, output = commands.getstatusoutput("cd %s && %s" % (self.root, command))
        # self.total_files = output.strip()

        # Get CLOC info.
        if include_cloc:
            command = Command("cloc %s --csv --quiet" % self.root)
            if command.run():

                # The cloc command produces output as below, but also produces extra output even with --quiet. So we
                # need to clean that up.
                """
                files, language, blank, comment, code
                13,CSS,2300,639,14631
                12,Javascript,828,393,2200
                9,HTML,72,155,1030
                13,SASS,19,22,928
                12,LESS,18,27,907
                5,XML,0,0,550
                3,JSON,0,0,3
                """
                for line in command.output.split("\n"):

                    values = line.split(",")

                    if values[0] == "":
                        continue

                    if values[0] == "files":
                        continue

                    files = values[0]
                    language = values[1]
                    code = values[4]

                    self.languages[language] = (files, code)

            # command = "cloc --csv --quiet %s" % self.root
            # status, output = commands.getstatusoutput(command)

        return self.is_loaded

    def path_exists(self, *args):
        """Determine if a given file or directory exists relative to the project's root."""
        path = os.path.join(self.root, *args)
        return os.path.exists(path)

    def to_csv(self, include_header=False):
        """Convert project attributes to CSV text output.

        :rtype: str

        .. note::
            Project attributes are returned in alphabetical order with form of ``name:value``. Language stats are
            returned at the end of the output.

        """
        lines = list()

        # Create the header if requested.
        if include_header:
            line = [
                "title",
                "category",
                "config file",
                "branch",
                "description",
                "description file",
                "directories",
                "dirty",
                "disk",
                "gitignore",
                "files",
                "license",
                "license file",
                "makefile",
                "manifest",
                "organization",
                "readme",
                "repo",
                "requirements",
                "setup",
                "status",
                "tags",
                "type",
                "version",
                "version file",
            ]

            if self.languages:
                for language in self.languages.keys():
                    line.append("%s files" % language)
                    line.append("%s LoC" % language)

            lines.append(",".join(line))

        # Create the line.
        line = list()

        line.append('"%s"' % self.title)
        line.append('"%s"' % self.category)
        line.append('"%s"' % bool_to_yes_no(self.config_exists))
        line.append('"%s"' % self.branch)
        line.append('"%s"' % self.description)
        line.append('"%s"' % bool_to_yes_no(self.description_exists))
        line.append('"%s"' % self.total_directories)
        line.append('"%s"' % bool_to_yes_no(self.is_dirty))
        line.append('"%s"' % self.disk)
        line.append('"%s"' % bool_to_yes_no(self.gitignore_exists))
        line.append('"%s"' % self.total_files)
        line.append('"%s"' % self.license)
        line.append('"%s"' % bool_to_yes_no(self.license_exists))
        line.append('"%s"' % bool_to_yes_no(self.makefile_exists))
        line.append('"%s"' % bool_to_yes_no(self.manifest_exists))
        line.append('"%s"' % self.org)
        line.append('"%s"' % bool_to_yes_no(self.readme_exists))
        line.append('"%s"' % self.scm)
        line.append('"%s"' % bool_to_yes_no(self.requirements_exists))
        line.append('"%s"' % bool_to_yes_no(self.setup_exists))
        line.append('"%s"' % self.status)
        line.append('"%s"' % "|".join(self.tags))
        line.append('"%s"' % self.type)
        line.append('"%s"' % self.version)
        line.append('"%s"' % bool_to_yes_no(self.version_exists))

        lines.append(",".join(line))
        print lines

        return "\n".join(lines)

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
        a.append("**Category**: %s  " % self.category)
        a.append("**Type**: %s  " % self.type)
        a.append("**Disk Usage**: %s  " % self._get_disk())
        a.append("**Source Code Management**: %s  " % self.scm)

        if self.tags:
            a.append("**Tags**: %s  " % ",".join(self.tags))

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
        a.append("## Requirements")
        a.append("")

        # get_requirements() may return a list of packages or list of URLs or package names. We want to distinguish
        # between the two and output accordingly.
        if self.has_packages_ini:
            for env in ENVIRONMENTS:
                packages = self.get_requirements(env=env)

                if len(packages) == 0:
                    continue

                a.append("### %s" % env)
                a.append("")

                for p in packages:
                    a.append(p.to_markdown())
        else:
            packages = self.get_requirements()
            for p in packages:
                a.append("- %s" % p)

            a.append("")

        # Include the project tree.
        a.append("## Tree")
        a.append("")

        a.append("**Directories:** %s" % self.total_directories)
        a.append("**Files:** %s" % self.total_files)
        a.append("")

        if self.languages:
            a.append("### Languages")
            a.append("")

            for language, stats in self.languages.items():
                files = "%s files" % stats[0]
                loc = "%s lines of code" % stats[1]

                a.append("%s: %s" % (language, files + ", " + loc))

            a.append("")

        tree = self.get_tree()
        for line in tree.split("\n"):
            a.append("    %s" % line)

        a.append("")

        return "\n".join(a)

    def to_stat(self, color=False):
        """Convert project attributes to a stat-style output.

        :param color: Indicates whether color should be applied to errors and warnings.
        :type color: bool

        :rtype: str

        """
        a = list()

        a.append(self.title)
        a.append("=" * 80)

        if self.description:
            if len(self.description) > 80:
                desc = self.description[:-15] + " ..."
            else:
                desc = self.description
            a.append(desc)
            a.append("-" * 80)
        else:
            a.append("description file: %s" % bool_to_yes_no(
                self.description_exists,
                color_enabled=color,
                color_no=yellow
            ))

        a.append("%-40s %s" % ("config file", bool_to_yes_no(
            self.config_exists,
            color_enabled=color,
            color_no=red,
            color_yes=green
        )))
        a.append("%-40s %s" % ("status", self.status))
        a.append("%-40s %s" % ("category", self.category))
        a.append("%-40s %s" % ("type", self.type))
        a.append("%-40s %s" % ("tags", ", ".join(self.tags)))
        a.append("%-40s %s" % ("version", self.version))
        a.append("%-40s %s" % ("version file", bool_to_yes_no(self.readme_exists)))
        a.append("." * 80)

        a.append("License")
        a.append("." * 80)
        a.append("%-40s %s" % ("license", self.license))
        a.append("%-40s %s" % ("license file", bool_to_yes_no(
            self.license_exists,
            color_enabled=color, color_no=yellow
        )))
        a.append("." * 80)

        a.append("Repo")
        a.append("." * 80)
        a.append("%-40s %s" % ("type", self.scm))
        a.append("%-40s %s" % ("gitignore", bool_to_yes_no(self.gitignore_exists)))
        a.append("%-40s %s" % ("branch", self.branch))
        a.append("%-40s %s" % ("dirty", bool_to_yes_no(self.is_dirty, color_enabled=color, color_yes=yellow)))
        a.append("." * 80)

        a.append("Setup")
        a.append("." * 80)
        a.append("%-40s %s" % ("readme", bool_to_yes_no(self.readme_exists, color_enabled=color, color_no=red)))
        a.append("%-40s %s" % ("manifest", bool_to_yes_no(self.manifest_exists, color_enabled=color, color_no=yellow)))
        a.append("%-40s %s" % ("requirements file", bool_to_yes_no(self.requirements_exists)))
        a.append("%-40s %s" % ("setup.py file", bool_to_yes_no(self.setup_exists)))
        a.append("%-40s %s" % ("makefile", bool_to_yes_no(self.makefile_exists)))
        a.append("." * 80)

        a.append("Disk")
        a.append("." * 80)
        a.append("%-40s %s" % ("disk", self.disk))
        a.append("%-40s %s" % ("directories", self.total_directories))
        a.append("%-40s %s" % ("files", self.total_files))
        a.append("." * 80)

        a.append("Languages")
        a.append("." * 80)
        if self.languages:
            for language, stats in self.languages.items():
                files = "%s files" % stats[0]
                loc = "%s lines of code" % stats[1]

                a.append("%-40s %s" % (language, files + ", " + loc))
        else:
            a.append("%-40s %s" % ("langauges", "None"))

        a.append("." * 80)

        a.append("Requirements")
        a.append("." * 80)

        if self.has_packages_ini:
            for env in ENVIRONMENTS:
                packages = self.get_requirements(env=env)

                if len(packages) == 0:
                    continue

                for p in packages:
                    if p.has_attribute("url"):
                        a.append(p.url)
                    else:
                        a.append(p.name)
        else:
            packages = self.get_requirements()
            for p in packages:
                a.append(p)

        a.append("." * 80)

        return "\n".join(a)

    def to_txt(self):
        """Convert project attributes to plain text output.

        :rtype: str

        .. note::
            Project attributes are returned in alphabetical order with form of ``name:value``. Language stats are
            returned at the end of the output.

        """
        a = list()
        a.append("category: %s" % self.category)
        a.append("config file: %s" % bool_to_yes_no(self.config_exists))
        a.append("branch: %s" % self.branch)
        a.append("description: %s" % self.description)
        a.append("description file: %s" % bool_to_yes_no(self.description_exists))
        a.append("directories: %s" % self.total_directories)
        a.append("dirty: %s" % bool_to_yes_no(self.is_dirty))
        a.append("disk: %s" % self.disk)
        a.append("gitignore: %s" % bool_to_yes_no(self.gitignore_exists))
        a.append("files: %s" % self.total_files)
        a.append("license: %s" % self.license)
        a.append("license file: %s" % bool_to_yes_no(self.license_exists))
        a.append("makefile: %s" % bool_to_yes_no(self.makefile_exists))
        a.append("manifest: %s" % bool_to_yes_no(self.manifest_exists))
        a.append("organization: %s" % self.org)
        a.append("readme: %s" % bool_to_yes_no(self.readme_exists))
        a.append("repo: %s" % self.scm)
        a.append("requirements: %s" % bool_to_yes_no(self.requirements_exists))
        a.append("setup: %s" % bool_to_yes_no(self.setup_exists))
        a.append("status: %s" % self.status)
        a.append("tags: %s" % ", ".join(self.tags))
        a.append("title: %s" % self.title)
        a.append("type: %s" % self.type)
        a.append("version: %s" % self.version)
        a.append("version file: %s" % bool_to_yes_no(self.readme_exists))

        if self.languages:
            for language, stats in self.languages.items():
                a.append("%s: %s files, %s lines of code" % (language, stats[0], stats[1]))
        else:
            a.append("langauges: None")
        return "\n".join(a)

    def _get_disk(self):
        """Return the result of the du command (cleaned up).

        :rtype str

        """
        # Throws a key error because of "print".
        # command = Command("du -hs %s | awk -F ' ' '{print $1}'", path=self.root)

        command = Command("du -hs", path=self.root)
        if command.run():
            return command.output.split("\t")[0].strip()
        else:
            return "UNKNOWN"

    def _get_org(self):
        """Get the organization identifier.

        :rtype: str

        .. note::
            The client is checked first, then the business. The ``code`` attribute is returned.

        """
        if self.has_client:
            return self.client.code
        elif self.has_business:
            return self.business.code
        else:
            return "???"

    def _get_path(self, name):
        return os.path.join(self.root, name)

    def _get_scm(self):
        """Determine the SCM in use and get the current state.

        :rtype: str | None
        :returns: Returns the type of SCM in use or ``None`` if no SCM is recognized.

        """
        if self.path_exists(".git"):

            # Determine whether the repo is dirty.
            # See http://stackoverflow.com/a/5737794/241720
            command = Command('cd %s && git status --porcelain' % self.root)
            command.run()

            if len(command.output) > 0:
                self.is_dirty = True
            else:
                self.is_dirty = False

            # Get the current branch name.
            command = Command("cd %s && git rev-parse --abbrev-ref HEAD" % self.root)
            if command.run():
                self.branch = command.output
            else:
                self.branch = "UNKNOWN"

            return "git"
        elif self.path_exists(".hg"):

            # Determine whether the repo is dirty.
            # See http://stackoverflow.com/a/11012582/241720
            command = Command("hg identify --id | grep --quiet + ; echo $?)", path=self.root)
            command.run()
            if command.status >= 1:
                self.is_dirty = True
            else:
                self.is_dirty = False

            # Get the current branch name.
            Command("hg branch", path=self.root)
            if command.run():
                self.branch = command.output
            else:
                self.branch = "UNKNOWN"

            return "hg"
        elif self.path_exists(".svn"):
            command = Command("test -z svn status", path=self.root)
            command.run()
            if command.status >= 1:
                self.is_dirty = True
            else:
                self.is_dirty = False

            # TODO: Parse output of svn info to get the current branch if possible.

            return "svn"
        else:
            return None

    def _load_section(self, name, values):
        """Overridden to add business, client, and project section values to the current instance."""
        if name == "business":
            try:
                organization_name = values.pop("name")
            except KeyError:
                organization_name = "Unknown"

            section = Business(organization_name, **values)
            setattr(self, name, section)
        elif name == "client":
            try:
                organization_name = values.pop("name")
            except KeyError:
                organization_name = "Unknown"

            section = Client(organization_name, **values)
            setattr(self, name, section)
        elif name == "project":
            for key in values.keys():
                setattr(self, key, values[key])
        elif name == "urls":
            section = Tools(name, **values)
            self._sections.append(name)
            setattr(self, name, section)
        else:
            super(Project, self)._load_section(name, values)

    def _load_version(self):
        """Get project version info.

        :rtype: str
        :returns: Returns the version string.

        .. note::
            This method sets the ``version``, ``version_py``, and ``version_txt`` attributes.

        """
        # Always set version_txt whether it exists or not. This allows it to be created if it does not already exist.
        self.version_txt = os.path.join(self.root, "VERSION.txt")
        if os.path.exists(self.version_txt):
            self.version = read_file(self.version_txt).strip()
        else:
            self.version = "0.1.0-d"

        # Set the path to the version.py file.
        self.version_py = None
        locations = (
            os.path.join(self.root, "version.py"),
            os.path.join(self.root, self.name, "version.py"),
            os.path.join(self.root, "source", "main", "version.py"),
        )
        for i in locations:
            if os.path.exists(i):
                self.version_py = i
                break


class Tools(Section):
    """Document the tools (URLs) used by a project."""

    def __init__(self, key, **kwargs):
        context = {}
        for category, icon in LINK_CATEGORIES:
            if category in kwargs:
                context[category] = kwargs[category]

        super(Tools, self).__init__(key, **context)

    def get_links(self):
        """Get the link from the tools/urls section.

        :rtype: list

        """
        a = list()
        for category, url in self._context.items():
            link = Link(url, category=category)
            a.append(link)

        return a
