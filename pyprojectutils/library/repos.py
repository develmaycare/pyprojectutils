"""

.. versionadded:: 0.23.0-d

"""

# Imports

import base64
import json
import os
# noinspection PyCompatibility
import urllib2
from github import Github
from .config import Config
from .constants import BITBUCKET_SCM, BITBUCKET_PASSWORD, BITBUCKET_USER, DEFAULT_SCM, GITHUB_PASSWORD, GITHUB_SCM, \
    GITHUB_USER, REPO_META_PATH

# Exports

__all__ = (
    "get_bitbucket_repos",
    "get_github_repos",
    "get_repos",
    "Repo",
)

# Functions


def get_bitbucket_repos():
    """Get repo meta data from the Bitbucket server.

    :rtype: list
    :raises urllib2.HTTPError

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
        repo = Repo(
            d['slug'],
            cli=d['scm'],
            host="bitbucket.org",
            is_private=d['is_private'],
            user=d['owner']
        )
        repos.append(repo)

    # Return the repos.
    return repos


def get_github_repos():
    """Get GitHub repos from the GitHub server.

    :rtype: list

    """
    # Initialize the connection to github.
    gh = Github(GITHUB_USER, GITHUB_PASSWORD)

    # Seems like loading the user is required to get at the other data.
    user = gh.get_user()

    # Get the repo instance.
    repos = list()
    results = user.get_repos()
    for result in results:
        repo = Repo(
            result.name,
            cli="git",
            host="github.com",
            is_private=result.private,
            user=result.owner.name
        )
        repos.append(repo)

    return repos


def get_repos(all=False, criteria=None, path=REPO_META_PATH):
    """Get the available repos.

    :param all: List all (even remote) repos.
    :type all: bool

    :param path: Path to where projects are stored.
    :type path: str

    :param criteria: Criteria used to filter the list, if any.
    :type criteria: dict

    :rtype: list[Repo]

    """
    names = list()
    repos = list()

    # Get remote repos.
    if all:
        # Get repos from remote services.
        try:
            remotes = get_bitbucket_repos() + get_github_repos()
        except urllib2.HTTPError:
            remotes = list()

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
        repo = Repo(repo_name, full_path)
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
                    tags = getattr(repo, "tags")
                    if search in tags:
                        filtered_repos.append(repo)
                else:
                    value = getattr(repo, field)
                    if search == value:
                        filtered_repos.append(repo)
        return filtered_repos
    else:
        return repos


# Classes


class Repo(Config):
    """Represents a source code repository."""

    def __init__(self, name, cli="git", host=DEFAULT_SCM, is_private=None, path=None, project=None, user=None):
        # Set the standard repo properties.
        self.host = None
        self.is_private = None
        self.name = None
        self.path = None
        self.project = None
        self.type = None
        self.user = None
        
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
