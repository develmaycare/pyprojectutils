"""

Variables, as distinct from constants, change with the local environment. Defaults, if any, are established here if no
value exists in the local environment.

.. versionadded:: 0.34.0-d

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

Default: ``ANON``

A short code or abbreviation of your name or development company.

``DEVELOPER_NAME``
------------------

Default: ``Anonymous``

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

Default: ``$PROJECT_HOME/.archive``

Where projects are archived. Additional scripts may be written to further process projects in this directory.

``PROJECT_HOME``
----------------

Default: ``~/Work``

Where active projects are stored.

``PROJECTS_ON_HOLD``
--------------------

Default: ``$PROJECT_HOME/.hold``

Where inactive projects are stored.

``REPO_META_PATH``
------------------

Default: ``$PROJECT_HOME/.repos``

Meta data (``repo.ini`` files) are stored where by ``checkoutproject``.

``TEMPLATE_PATH``
-----------------

Default: ``$PYTHON_HOME/pyprojectutils/templates``

.. versionchanged:: 0.34.1-d
    These variables were migrated from ``constants``.

The path to pyprojectutils templates. Used by the ``initproject`` command. This forms the basis for various other
template variables:

- ``GITIGNORE_TEMPLATE``: The template used for creating a project's ``.gitignore`` file.
- ``MANIFEST_TEMPLATE``: The template used for creating a project's ``MANIFEST.in`` file.
- ``PROJECT_INI_TEMPLATE``: The template used for creating a project's ``project.ini`` file.
- ``README_TEMPLATE``: The template used for creating a project's ``README.markdown`` file.
- ``REQUIREMENTS_TEMPLATE``: The template used for creating a project's ``requirements.pip`` file. The default file is
  blank, but you may override the template to incorporate your own processing.

"""
# Imports

import os

# NOTE: Since these are specific to each user, you *must* document the variables above. Otherwise the defaults will
# appear in the documentation.
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
    "GITIGNORE_TEMPLATE",
    "MANIFEST_TEMPLATE",
    "PROJECT_ARCHIVE",
    "PROJECT_HOME",
    "PROJECT_INI_TEMPLATE",
    "PROJECTS_ON_HOLD",
    "README_TEMPLATE",
    "REQUIREMENTS_TEMPLATE",
    "TEMPLATE_PATH",
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

# Templates. Especially for initproject.
TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")

GITIGNORE_TEMPLATE = os.path.join(TEMPLATE_PATH, "gitignore.j2")

MANIFEST_TEMPLATE = os.path.join(TEMPLATE_PATH, "manifest.in.j2")

PROJECT_INI_TEMPLATE = os.path.join(TEMPLATE_PATH, "project.ini.j2")

README_TEMPLATE = os.path.join(TEMPLATE_PATH, "readme.markdown.j2")

REQUIREMENTS_TEMPLATE = os.path.join(TEMPLATE_PATH, "requirements.pip.j2")
