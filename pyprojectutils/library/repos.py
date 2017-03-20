"""

.. versionadded:: 0.23.0-d

"""

# Imports

import base64
import json
import os
# noinspection PyCompatibility
import urllib2
# noinspection PyPackageRequirements
from github import Github
from .config import Config
from .constants import BITBUCKET_SCM, DEFAULT_SCM, GITHUB_SCM
from .exceptions import CommandFailed, InputError, ResourceUnavailable
from .shell import Command
from .variables import BITBUCKET_PASSWORD, BITBUCKET_USER, GITHUB_PASSWORD, GITHUB_USER, PROJECT_ARCHIVE, \
    PROJECT_HOME, PROJECTS_ON_HOLD, REPO_META_PATH

# Exports

__all__ = (
    "create_local_repo",
    "create_remote_repo",
    "get_bitbucket_repos",
    "get_github_repos",
    "get_repos",
    "Repo",
)

# Functions


def create_local_repo(path, add=True, cli="git", commit=False, message="Initial Import"):
    """Create a repo on the given path.

    :param cli: The type of repo to create; ``git``, ``hg``, ``svn``.
    :type cli: str

    :param path: The path to the repo (project).
    :type path: str

    :param add: Whether to add existing files.
    :type add: bool

    :param commit: Whether to also commit files.
    :type commit: bool

    :param message: The commit message.
    :type message: str

    :rtype: BaseRepo

    .. versionadded:: 0.34.4-d

    .. versionchanged:: 0.34.4-d
        Added ``cli`` parameter.

    .. note::
        Only git and hg are currently supported.

    """
    # We can't do anything if the project does not exist.
    if not os.path.exists(path):
        raise InputError("Local repo path does not exist: %s" % path)

    # Run the init.
    if cli == "git":
        command = Command("git init", path=path)
    elif cli == "hg":
        command = Command("hg init", path=path)
    else:
        raise CommandFailed("Unsupported CLI: %s" % cli)

    if not command.run():
        raise CommandFailed("Failed to run %s: %s" % (command.string, command.output))

    # Add files.
    if add:
        if cli == "git":
            command = Command("git add .", path=path)
        elif cli == "hg":
            command = Command("hg add", path=path)
        else:
            raise CommandFailed("Unsupported CLI: %s" % cli)

        if not command.run():
            raise CommandFailed("Failed to run %s: %s" % (command.string, command.output))

    # Commit.
    if commit:
        if cli == "git":
            command = Command('git commit -m "%s"' % message)
        elif cli == "hg":
            command = Command('hg commit -m "%s"' % message)
        else:
            raise CommandFailed("Unsupported CLI: %s" % cli)

        if not command.run():
            raise CommandFailed("Failed to run %s: %s" % (command.string, command.output))

    # Return the repo instance.
    return BaseRepo(os.path.basename(path), cli=cli)


def create_remote_repo(name, cli="git", description=None, has_issues=False, has_wiki=False, is_private=False,
                       vendor=DEFAULT_SCM):
    """Create a remote repo.

    :param name: The repo name.
    :type name: str

    :param cli: The type of repo to create; ``git``, ``hg``, ``svn``. Not that not all vendors support all repo types.
    :type cli: str

    :param description: Description of the repo.
    :type description: str

    :param is_private: Indicates the repo should be private.
    :type is_private: bool

    :param has_issues: Indicates the repo should include issues.
    :type has_issues: bool

    :param has_wiki: Indicates the repo should include issues.
    :type has_wiki: bool

    :param vendor: The SCM vendor to use. Defaults to the ``DEFAULT_SCM`` environment variable.
    :type vendor: str

    :rtype: Repo

    .. versionadded:: 0.34.0-d

    .. versionchanged:: 0.34.4-d
        Added ``cli`` parameter. This will be silently ignored by vendors that don't support different repo types.

    """
    if vendor in ("github.com", "github", "gh"):
        repo = GitHubRepo(
            name,
            description=description,
            has_issues=has_issues,
            has_wiki=has_wiki,
            is_private=is_private
        )

        try:
            repo.create()
        except ResourceUnavailable as e:
            raise CommandFailed("Could not create the GitHub repo: %s" % e.message)

        return repo
    elif vendor in ("bitbucket.org", "bitbucket", "bb"):
        repo = BitbucketRepo(
            name,
            cli=cli,
            description=description,
            has_issues=has_issues,
            has_wiki=has_wiki,
            is_private=is_private
        )

        try:
            repo.create()
        except ResourceUnavailable as e:
            raise CommandFailed("Could not create the Bitbucket repo: %s" % e.message)

        return repo
    else:
        raise CommandFailed("SCM vendor is not currently supported: %s" % vendor)


# noinspection SpellCheckingInspection
def get_bitbucket_repos():
    """Get repo meta data from the Bitbucket server.

    :rtype: list[BitbucketRepo]
    :raises: urllib2.HTTPError

    .. versionchanged:: 0.34.4-d
        The return value is now a list of :py:class:`BitbucketRepo` instances.

    """

    # Get results from the API.
    request = urllib2.Request("https://api.bitbucket.org/1.0/user/repositories/")
    base64string = base64.encodestring('%s:%s' % (BITBUCKET_USER, BITBUCKET_PASSWORD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    result = urllib2.urlopen(request)

    # Convert the JSON and create a repo instance for each repo found.
    data = json.loads(result.read())
    repos = list()
    for d in data:
        repo = BitbucketRepo(
            d['slug'],
            cli=d['scm'],
            host="bitbucket.org",
            is_private=d['is_private'],
            user=d['owner']
        )
        repos.append(repo)

    # Return the repos.
    return repos


# noinspection SpellCheckingInspection
def get_github_repos():
    """Get GitHub repos from the GitHub server.

    :rtype: list[GitHubRepo]

    .. versionchanged:: 0.34.4-d
        The return value is now a list of :py:class:`GitHubRepo` instances.

    """

    # Initialize the connection to github.
    gh = Github(GITHUB_USER, GITHUB_PASSWORD)

    # Seems like loading the user is required to get at the other data.
    user = gh.get_user()

    # Get the repo instance.
    repos = list()
    results = user.get_repos()
    for result in results:
        repo = GitHubRepo(
            result.name,
            cli="git",
            host="github.com",
            is_private=result.private,
            user=result.owner.name
        )
        repos.append(repo)

    return repos


# noinspection SpellCheckingInspection
def get_repos(criteria=None, path=REPO_META_PATH, show_all=False):
    """Get the available repos.

    :param criteria: Criteria used to filter the list, if any.
    :type criteria: dict

    :param path: Path to where projects are stored.
    :type path: str

    :param show_all: List all (even remote) repos.
    :type show_all: bool

    :rtype: list[BaseRepo | BitbucketRepo | GitHubRepo], list
    :returns: A list with two lists; the first list is a list of repo instances while the second list is any errros that
              occurred during processing.

    .. versionchanged:: 0.34.4-d
        Changed ``all`` to ``show_all`` to avoid shadowing a built-in name. The instances returned are also the
        appropriate class, or :py:class:`BaseRepo` if not specific host is available.

    """
    errors = list()
    names = list()
    repos = list()

    # Get remote repos.
    remotes = list()
    if show_all:
        # Get repos from remote services.
        try:
            remotes += BitbucketRepo.fetch()
        except urllib2.HTTPError as e:
            errors.append("Failed to get Bitbucket repos: %s" % e.message)

        try:
            remotes += GitHubRepo.fetch()
        except urllib2.HTTPError as e:
            errors.append("Failed to get GitHub repos: %s" % e.message)

        # Prepare to sort repos by name.
        repo_dict = dict()
        for repo in remotes:
            names.append(repo.name)
            repo_dict[repo.name] = repo

        names.sort()

        # Create the list of repos.
        for repo_name in names:
            repos.append(repo_dict[repo_name])

    # Get the repos from meta data.
    entries = os.listdir(path)
    for entry in entries:

        # Skip DS_Store.
        if entry == ".DS_Store":
            continue

        # Repos are always stored as an INI file.
        full_path = os.path.join(path, entry)
        if not os.path.isfile(full_path):
            continue

        # The repo name is the entry without the ini extension.
        repo_name = entry[:-4]

        # Skip repos we've already found.
        if repo_name in names:
            continue

        # Load the repo.
        repo = BaseRepo(repo_name, path=full_path)
        repo.load()
        repos.append(repo)
        # print(repo)

    # Filter based on criteria, which should be a dict.
    if criteria:
        filtered_repos = list()
        for repo in repos:

            for field, search in criteria.items():

                # Handle the name and description attributes differently.
                if field in ("description", "name"):
                    value = getattr(repo, field).lower()
                    search = search.lower()
                    if search in value:
                        filtered_repos.append(repo)
                elif field == "tag":
                    tags = getattr(repo, "tags", list())
                    if search in tags:
                        filtered_repos.append(repo)
                else:
                    value = getattr(repo, field)
                    if search == value:
                        filtered_repos.append(repo)
        return filtered_repos, errors
    else:
        return repos, errors


# Classes


class Repo(Config):
    """Represents a source code repository."""

    def __init__(self, name, cli="git", description=None, has_issues=None, has_wiki=None, host=DEFAULT_SCM,
                 is_private=None, path=None, project=None, user=None):
        # Set the standard repo properties.
        self.cli = cli
        self.description = description
        self.has_issues = has_issues
        self.has_wiki = has_wiki
        self.host = host
        self.is_private = is_private
        self.name = name
        self.path = path
        self.project = project
        self.type = cli
        self.user = user
        
        # Load an existing configuration, or populate values from init parameters.
        if path and os.path.exists(path):
            super(Repo, self).__init__(path)
            self.load()
        else:
            path = os.path.join(REPO_META_PATH, "%s.ini" % name)
            super(Repo, self).__init__(path)

            self.is_private = is_private
            self.name = name
            self.project = project or name
            self.type = cli

            if user:
                self.host = host
                self.user = user
            elif host in ("bitbucket.org", "bitbucket", "bb"):
                self.host = BITBUCKET_SCM
                self.user = BITBUCKET_USER
            elif host in ("github.com", "github", "gh"):
                self.host = GITHUB_SCM
                self.user = GITHUB_USER
            else:
                self.host = host
                self.user = None

    def create(self):
        """Create a remote repo.

        .. versionadded:: 0.34.0-d

        """
        raise NotImplementedError()

    def get_command(self):
        """Get the command that will download/clone the repo.

        :rtype: str

        """
        # TODO: Implement command support for SVN and HG.
        return "git clone git@%s:%s/%s.git" % (self.host, self.user, self.name)

    def get_url(self):
        """Get the URL of the repo.

        :rtype: str

        .. versionadded:: 0.27.3-d

        """
        if self.host in ("bitbucket.org", "github.com"):
            return "https://%s/%s/%s" % (self.host, self.user, self.name)
        elif self.host == "codebasehq":
            # https://ptltd.codebasehq.com/projects/basis-hr/repositories/basishr_app/tree/master
            return "https://%s/projects/%s/repositories/%s/tree/master" % (
                self.host,
                self.user,
                self.project
            )
        else:
            return "https://%s/%s" % (self.host, self.name)

    def init(self, add=True, commit=False, message="Initial Import"):
        """Create a repo on the given path.

        :param path: The path to the repo (project).
        :type path: str

        :param add: Whether to add existing files.
        :type add: bool

        :param commit: Whether to also commit files.
        :type commit: bool

        :param message: The commit message.
        :type message: str

        :rtype: Repo

        .. versionadded:: 0.34.4-d

        .. note::
            Only git is currently supported.

        """
        raise NotImplementedError()

    def to_string(self):

        a = list()
        a.append("[repo]")
        a.append("host = %s" % self.host)
        a.append("name = %s" % self.name)
        a.append("project = %s" % self.project or "")
        a.append("type = %s" % self.type)
        a.append("user = %s" % self.user or "")

        output = "\n".join(a)
        output += super(Repo, self).to_string()

        return output

    @property
    def url(self):
        """Alias of ``get_url()``."""
        return self.get_url()

    def _load_section(self, name, values):
        """Overridden to deal with repo section values to the current instance."""
        # We only expect a section for the repo, but will allow other sections to be dynamically added at run time.
        if name == "repo":
            for key in values.keys():
                setattr(self, key, values[key])
        else:
            super(Repo, self)._load_section(name, values)


class BaseRepo(Config):
    """Represents a source code repository.

    .. versionadded:: 0.34.4-d

    """

    def __init__(self, name, cli="git", description=None, has_issues=None, has_wiki=None, host=DEFAULT_SCM,
                 is_private=None, path=None, project=None, user=None):
        """Initialize a repo.

        :param name: The name (slug) of the repo. Note this is (or should be) the same as the project name.
        :type name: str

        :param cli: The type of repo as represented by the command line tool; ``git``, ``hg``, or ``svn``.
        :type cli: str

        :param description: The description of the repo.  Note this is (or should be) the same as that of the project.
        :type description: str

        :param has_issues: Indicates whether issue management is enabled on the host.
        :type has_issues: bool

        :param has_wiki: Indicates whether the WIKI is enabled on the host.
        :type has_wiki: bool

        :param host: The host of the repo.
        :type host: str

        :param is_private: Indicates the repo is private.
        :type is_private: bool

        :param path: The path to the ``repo.ini`` file.
        :type path: str

        :param project: The project instance. This is required for ``init()``.
        :type project: Project

        :param user: The user (owner) of the repo. This is typically the handle used with the host.
        :type user: str

        .. note::
            We use ``cli`` because ``type`` would conflict with the built-in of the same name. ``type`` is available as
            as property, which returns the value of ``cli``.

        """
        # Set the standard repo properties so that we can reference them in the IDE. We take the parameters from init,
        # but these may be overridden below if the a config file exists.
        self.cli = cli
        self.description = description
        self.has_issues = has_issues
        self.has_wiki = has_wiki
        self.host = host
        self.is_private = is_private
        self.name = name
        self.project = project
        self.user = user

        # The given path may exist, but we also want to auto-discover the path.
        if path and os.path.exists(path):
            config_path = path
        else:
            config_path = os.path.join(REPO_META_PATH, "%s.ini" % name)

        # Initialize the underlying config. This is safe because no additional processing occurs until load() is called.
        super(BaseRepo, self).__init__(config_path)

        # Set host and user values from aliases.
        if host in ("bitbucket.org", "bitbucket", "bb"):
            self.host = BITBUCKET_SCM

            if not user:
                self.user = BITBUCKET_USER
        elif host in ("github.com", "github", "gh"):
            self.host = "github.com"

            if not user:
                self.user = GITHUB_USER
        else:
            pass

        # If a project is given, we can set description if it has not also been given.
        if project and not description:
            self.description = project.description

        # Determine if the repo exists as a project on the local machine.
        if project:
            self.is_local = True
            self.location = "local"
        elif os.path.exists(os.path.join(PROJECT_HOME, name)):
            self.is_local = True
            self.location = "local"
        elif os.path.exists(os.path.join(PROJECTS_ON_HOLD, name)):
            self.is_local = True
            self.location = "hold"
        elif os.path.exists(os.path.join(PROJECT_ARCHIVE, name)):
            self.is_local = True
            self.location = "archive"
        else:
            self.is_local = False
            self.location = "remote"

    def create(self):
        """Create a remote repo.

        .. versionadded:: 0.34.0-d

        """
        raise NotImplementedError()

    def get_command(self):
        """Get the command that will download/clone the repo.

        :rtype: str

        """
        # TODO: Implement command support for SVN and HG.
        return "git clone git@%s:%s/%s.git" % (self.host, self.user, self.name)

    def get_url(self):
        """Get the URL of the repo.

        :rtype: str

        .. versionadded:: 0.27.3-d

        """
        if self.host in ("bitbucket.org", "github.com"):
            return "https://%s/%s/%s" % (self.host, self.user, self.name)
        elif self.host == "codebasehq":
            # https://ptltd.codebasehq.com/projects/basis-hr/repositories/basishr_app/tree/master
            return "https://%s/projects/%s/repositories/%s/tree/master" % (
                self.host,
                self.user,
                self.project
            )
        else:
            return "https://%s/%s" % (self.host, self.name)

    def init(self, add=True, commit=False, message="Initial Import"):
        """Create a repo on the given path.

        :param add: Whether to add existing files.
        :type add: bool

        :param commit: Whether to also commit files.
        :type commit: bool

        :param message: The commit message.
        :type message: str

        :rtype: Repo

        .. versionadded:: 0.34.4-d

        .. note::
            Only git is currently supported.

        """
        raise NotImplementedError()

    def to_string(self):

        a = list()
        a.append("[repo]")
        a.append("cli = %s" % self.cli)
        a.append("description = %s" % self.description)
        a.append("has_issues = %s" % self.has_issues)
        a.append("has_wiki = %s" % self.has_wiki)
        a.append("host = %s" % self.host)
        a.append("name = %s" % self.name)

        if self.user:
            a.append("user = %s" % self.user)

        output = "\n".join(a)
        output += super(BaseRepo, self).to_string()

        return output

    @property
    def type(self):
        """Alias for ``cli``."""
        return self.cli

    @property
    def url(self):
        """Alias of ``get_url()``."""
        return self.get_url()

    def _load_section(self, name, values):
        """Overridden to deal with repo section values to the current instance."""
        # We only expect a section for the repo, but will allow other sections to be dynamically added at run time.
        if name == "repo":
            for key in values.keys():
                setattr(self, key, values[key])
        else:
            super(BaseRepo, self)._load_section(name, values)


class BitbucketRepo(BaseRepo):
    """Represents a GitHub repo when the repo vendor is known at run time.

    .. versionadded:: 0.34.4-d

    """

    def __init__(self, name, cli="git", description=None, has_issues=None, has_wiki=None, host=DEFAULT_SCM,
                 is_private=None, path=None, project=None, user=None):
        super(BitbucketRepo, self).__init__(
            name,
            cli=cli,
            description=description,
            has_issues=has_issues,
            has_wiki=has_wiki,
            host="bitbucket.org",
            is_private=is_private,
            path=path,
            project=project,
            user=user
        )

    def init(self, add=True, commit=False, message="Initial Import"):
        """

        :raise: CommandFailed

        """

        if not self.project:
            raise CommandFailed("A Project instance is required.")

        if not os.path.exists(self.path):
            raise InputError("Local repo path does not exist: %s" % self.project.root)

        if self.cli == "git":
            command = Command("git init", path=self.project.root)
            if not command.run():
                raise CommandFailed("Failed to run git init: %s" % command.output)

            if add:
                command = Command("git add .", path=self.project.root)
                if not command.run():
                    raise CommandFailed("Failed to run git add: %s" % command.output)

            if commit:
                command = Command('git commit -m "%s"' % message)
                if not command.run():
                    raise CommandFailed("Failed to run git commit: %s" % command.output)
        else:
            raise CommandFailed("CLI not supported: %s" % self.cli)

        return True

    def create(self):

        # Assemble the data.
        data = {
            'has_issues': self.has_issues,
            'has_wiki': self.has_wiki,
            'is_private': self.is_private,
            'name': self.name,
            'scm': self.cli,
        }

        # Define the URL. See
        # https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Busername%7D/%7Brepo_slug%7D#post
        url = "https://api.bitbucket.org/2.0/repositories/%s/%s" % (self.user, self.name)

        # Get results from the API.

        request = urllib2.Request(url, data=data)
        base64string = base64.encodestring('%s:%s' % (BITBUCKET_USER, BITBUCKET_PASSWORD)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        result = urllib2.urlopen(request)

        # Convert the JSON and create a repo instance for each repo found.
        data = json.loads(result.read())

    @staticmethod
    def fetch():
        """Get repo meta data from the Bitbucket server.

        :rtype: list
        :raises: urllib2.HTTPError

        """

        # Get results from the API.
        request = urllib2.Request("https://api.bitbucket.org/1.0/user/repositories/")
        base64string = base64.encodestring('%s:%s' % (BITBUCKET_USER, BITBUCKET_PASSWORD)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        result = urllib2.urlopen(request)

        # Convert the JSON and create a repo instance for each repo found.
        data = json.loads(result.read())
        repos = list()
        for d in data:
            repo = BitbucketRepo(
                d['slug'],
                cli=d['scm'],
                has_issues=d['has_issues'],
                has_wiki=d['has_wiki'],
                is_private=d['is_private'],
                user=d['owner']
            )
            repos.append(repo)

        # Return the repos.
        return repos


class GitHubRepo(BaseRepo):
    """Represents a GitHub repo when the repo vendor is known at run time.

    .. versionadded:: 0.34.4-d

    """

    # noinspection PyUnusedLocal
    def __init__(self, name, cli="git", description=None, has_issues=None, has_wiki=None, host=GITHUB_SCM,
                 is_private=None, path=None, project=None, user=None):
        super(GitHubRepo, self).__init__(
            name,
            cli="git",
            description=description,
            has_issues=has_issues,
            has_wiki=has_wiki,
            host="github.com",
            is_private=is_private,
            path=path,
            project=project,
            user=user
        )

    @staticmethod
    def fetch():
        """Get GitHub repos from the GitHub server.

        :rtype: list[GitHubRepo]

        """

        # Initialize the connection to github.
        gh = Github(GITHUB_USER, GITHUB_PASSWORD)

        # Seems like loading the user is required to get at the other data.
        user = gh.get_user()

        # Get the repo instance.
        repos = list()
        results = user.get_repos()
        for result in results:
            repo = GitHubRepo(
                result.name,
                is_private=result.private,
                user=result.owner.name
            )
            repos.append(repo)

        return repos

    def init(self, add=True, commit=False, message="Initial Import"):
        """

        :raise: CommandFailed

        """

        if not self.project:
            raise CommandFailed("A Project instance is required.")

        if not os.path.exists(self.path):
            raise InputError("Local repo path does not exist: %s" % self.project.root)

        command = Command("git init", path=self.project.root)
        if not command.run():
            raise CommandFailed("Failed to run git init: %s" % command.output)

        if add:
            command = Command("git add .", path=self.project.root)
            if not command.run():
                raise CommandFailed("Failed to run git add: %s" % command.output)

        if commit:
            command = Command('git commit -m "%s"' % message)
            if not command.run():
                raise CommandFailed("Failed to run git commit: %s" % command.output)

        return True

    def create(self):

        try:
            # noinspection PyPackageRequirements
            from github import Github
        except ImportError:
            # noinspection PyPep8Naming,PyUnusedLocal,PyUnusedLocal,SpellCheckingInspection,PyShadowingNames
            Github = None
            raise ResourceUnavailable("PyGithub is required: pip install pygithub")

        # Load the API and get the authenticated user.
        gh = Github(GITHUB_USER, GITHUB_PASSWORD)
        user = gh.get_user()

        # Create the repo.
        user.create_repo(
            self.name,
            description=self.description,
            private=self.is_private,
            has_issues=self.has_issues
        )

