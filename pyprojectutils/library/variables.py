"""
.. versionadded:: 0.34.0-d

Variables, as distinct from constants, change with the local environment. Defaults, if any, are established here if no
value exists in the local environment.

``BITBUCKET_ENABLED``
---------------------

Default: ``False``

Bitbucket is enabled if a user and password has been set.

``BITBUCKET_PASSWORD``
----------------------

Default: ``None``

The Bitbucket password for ``BITBUCKET_USER``.

``BITBUCKET_USER``
------------------

Default: ``None``

The Bitbucket user name.

``DEVELOPER_CODE``
------------------

Default: ANON

A short code or abbreviation of your name or development company.

``DEVELOPER_NAME``
------------------

Default: Anonymous

Your name or the name of your development company.

``DOCUMENTATION_HOME``
----------------------

Default: ``~/Dropbox/Business/Documentation``

The location where documentation is stored.

``GITHUB_ENABLED``
------------------

Default: ``False``

GitHub is enabled if a user and password has been set.

``GITHUB_PASSWORD``
-------------------

Default: ``None``

The GitHub password for ``GITHUB_USER``.

``GITHUB_USER``
---------------

Default: ``None``

The GitHub user name.

``PROJECT_ARCHIVE``
-------------------

Default: $PROJECT_HOME/.archive

Where projects are archived. Additional scripts may be written to further process projects in this directory.

``PROJECT_HOME``
----------------

Default: ~/Work

Where active projects are stored.

``PROJECTS_ON_HOLD``
--------------------

Default: $PROJECT_HOME/.hold

Where inactive projects are stored.

``REPO_META_PATH``
------------------

Default: $PROJECT_HOME/.repos

Meta data (``repo.ini`` files) are stored where by ``checkoutproject``.

"""
# Imports

import os

# NOTE: Since these are specific to each user, you *must* document the variables above.
__all__ = (
    "DEVELOPER_CODE",
    "DEVELOPER_NAME",
    "DOCUMENTATION_HOME",
    "BITBUCKET_ENABLED",
    "BITBUCKET_PASSWORD",
    "BITBUCKET_USER",
    "GITHUB_ENABLED",
    "GITHUB_PASSWORD",
    "GITHUB_USER",
    "PROJECT_ARCHIVE",
    "PROJECT_HOME",
    "PROJECTS_ON_HOLD",
)

# The developer name is the name of an individual or company that creates and manages projects. The code is merely a
# short form of the name, such as an abbreviation. For example, we abbreviate Devel May Care as DMC.
DEVELOPER_CODE = os.environ.get("DEVELOPER_CODE", "ANON")
DEVELOPER_NAME = os.environ.get("DEVELOPER_NAME", "Anonymous")

# Documentation is stored in a specific location.
DOCUMENTATION_HOME = os.environ.get("DOCUMENTATION_HOME", os.path.expanduser("~/Dropbox/Business/Documentation"))

# Bitbucket integration requires a user name and password.
BITBUCKET_USER = os.environ.get("BITBUCKET_USER", None)
BITBUCKET_PASSWORD = os.environ.get("BITBUCKET_PASSWORD", None)

if BITBUCKET_USER and BITBUCKET_USER:
    BITBUCKET_ENABLED = True
else:
    BITBUCKET_ENABLED = False

# GitHub integration is only possible if the user sets a user and password in the local environment.
GITHUB_USER = os.environ.get("GITHUB_USER", None)

GITHUB_PASSWORD = os.environ.get("GITHUB_PASSWORD", None)

if GITHUB_USER and GITHUB_PASSWORD:
    GITHUB_ENABLED = True
else:
    GITHUB_ENABLED = False

# Location of projects. User home is automatically expanded.
PROJECT_HOME = os.environ.get("PROJECT_HOME", os.path.expanduser("~/Work"))

# Location of archived projects.
PROJECT_ARCHIVE = os.environ.get("PROJECT_ARCHIVE", os.path.join(PROJECT_HOME, ".archive"))

# Location of projects on hold.
PROJECTS_ON_HOLD = os.environ.get("PROJECTS_ON_HOLD", os.path.join(PROJECT_HOME, ".hold"))

# The path to repo.ini files.
REPO_META_PATH = os.environ.get("REPO_META_PATH", os.path.join(PROJECT_HOME, ".repos"))
