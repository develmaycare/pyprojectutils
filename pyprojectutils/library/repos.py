# Imports

import os
from .config import Config
from .constants import BITBUCKET_SCM, BITBUCKET_USER, DEFAULT_SCM, GITHUB_SCM, GITHUB_USER, REPO_META_PATH

# Exports

__all__ = (
    "Repo",
)

# Classes


class Repo(Config):
    """Represents a source code repository."""

    def __init__(self, name, cli="git", host=DEFAULT_SCM, path=None, project=None, user=None):
        # Set the standard repo properties.
        self.host = None
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

            self.name = name
            self.project = project or name
            self.type = cli

            if user:
                self.host = host
                self.user = user
            elif host in ("bitbucket", "bb"):
                self.host = BITBUCKET_SCM
                self.user = BITBUCKET_USER
            elif host in ("github", "gh"):
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

    @staticmethod
    def get_repos(criteria=None, path=REPO_META_PATH):
        """Get the available repos.
        
        :param path: Path to where projects are stored.
        :type path: str

        :param criteria: Criteria used to filter the list, if any.
        :type criteria: dict
        
        :rtype: list[Repo]
        
        """
        names = list()
        repos = list()

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
            # print(repo)

            # Filter based on criteria, which should be a dict.
            if criteria:
                for field, search in criteria.items():

                    # Handle the name and description attributes differently.
                    if field in ("description", "name"):
                        value = getattr(repo, field).lower()
                        search = search.lower()
                        if search in value:
                            repos.append(repo)
                    elif field == "tag":
                        tags = getattr(repo, "tags")
                        if search in tags:
                            repos.append(repo)
                    else:
                        value = getattr(repo, field)
                        if search == value:
                            repos.append(repo)
            else:
                repos.append(repo)

        return repos

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

    def _load_section(self, name, values):
        """Overridden to deal with repo section values to the current instance."""
        # We only expect a section for the repo, but will allow other sections to be dynamically added at run time.
        if name == "repo":
            for key in values.keys():
                setattr(self, key, values[key])
        else:
            super(Repo, self)._load_section(name, values)
