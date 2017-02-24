import os

__all__ = (
    "AUTHOR",
    "BASE_ENVIRONMENT",
    "BITBUCKET_ENABLED",
    "BITBUCKET_SCM",
    "BITBUCKET_USER",
    "BUSINESS",
    "CLIENT",
    "CONTROL_ENVIRONMENT",
    "DEFAULT_SCM",
    "DEVELOPMENT",
    "DEVELOPER_CODE",
    "DEVELOPER_NAME",
    "DEVELOPMENT_ENVIRONMENT",
    "DOCUMENTATION_HOME",
    "ENVIRONMENTS",
    "EXIT_ENV",
    "EXIT_INPUT",
    "EXIT_OK",
    "EXIT_OTHER",
    "EXIT_USAGE",
    "EXPERIMENTAL",
    "GITHUB_ENABLED",
    "GITHUB_PASSWORD",
    "GITHUB_SCM",
    "GITHUB_USER",
    "LICENSE_CHOICES",
    "LINK_CATEGORIES",
    "LIVE",
    "LIVE_ENVIRONMENT",
    "PROJECT_ARCHIVE",
    "PROJECT_HOME",
    "PROJECTS_ON_HOLD",
    "PUBLISHER",
    "REPO_META_PATH",
    "STAGING",
    "STAGING_ENVIRONMENT",
    "TESTING",
    "TESTING_ENVIRONMENT",
)

# The developer name is the name of an individual or company that creates and manages projects. The code is merely a
# short form of the name, such as an abbreviation. For example, we abbreviate Devel May Care as DMC.
DEVELOPER_CODE = os.environ.get("DEVELOPER_CODE", "UNK")
"""A short code or abbreviation of your name or development company."""

DEVELOPER_NAME = os.environ.get("DEVELOPER_NAME", "Unidentified")
"""Your name or the name of your development company."""

# Organization types help identify who is involved in a project.
BUSINESS = "business"
"""Identifies an object as a business organization."""

CLIENT = "client"
"""Identifies an object as a client organization."""

# Documentation may have an author and publisher.
AUTHOR = "author"
"""Identifies an object as an author (individual or organization)."""

PUBLISHER = "publisher"
"""Identifies an object as publisher (individual or organization)."""

# Documentation is stored in a specific location.
DOCUMENTATION_HOME = os.environ.get("DOCUMENTATION_HOME", os.path.expanduser("~/Dropbox/Business/Documentation"))
"""The location where documentation is stored."""

# Standard stage identifiers.
EXPERIMENTAL = "experimental"
"""Prototype, experimental. Use at your own risk."""

PLANNING = "planning"
"""Planning, specification, not even in development."""

DEVELOPMENT = "development"
"""Development. Unstable, untested."""

TESTING = "testing"
"""Code that is in alpha or beta. Ready for integration and tests."""

STAGING = "staging"
"""Code that is tested and (probably) ready for release."""

RELEASE = "release"
"""A release or release candidate."""

LIVE = "live"
"""The project is now a product. Maintenance and support mode."""

# Standard environments.
BASE_ENVIRONMENT = "base"
"""The base environment represents the common dependencies and circumstances across all other environments."""

CONTROL_ENVIRONMENT = "control"
"""The control environment is the local machine used for generating documentation and running deployments."""

DEVELOPMENT_ENVIRONMENT = "development"
"""The development environment is where code is developed and initially tested."""

TESTING_ENVIRONMENT = "testing"
"""The testing environment is where code is integrated and unit tests are performed."""

STAGING_ENVIRONMENT = "staging"
"""The staging environment is where QA and test occurs."""

LIVE_ENVIRONMENT = "live"
"""The live environment is where the finished product lives or is hosted."""

ENVIRONMENTS = (
    BASE_ENVIRONMENT,
    CONTROL_ENVIRONMENT,
    DEVELOPMENT_ENVIRONMENT,
    TESTING_ENVIRONMENT,
    STAGING_ENVIRONMENT,
    LIVE_ENVIRONMENT,
)
"""A list of recognized environments."""

# Exit codes.
EXIT_OK = 0
"""A normal (successful) exit."""

EXIT_USAGE = 1
"""Usage of the command is incorrect."""

EXIT_INPUT = 2
"""Correct usage of the command, but with bad input."""

EXIT_ENV = 3
"""Something about the local environment is not suitable for successfully running the command."""

EXIT_OTHER = 4
"""All other (unsuccessful) exits."""

# Location of projects. User home is automatically expanded.
PROJECT_HOME = os.environ.get("PROJECT_HOME", os.path.expanduser("~/Work"))
"""Where active projects are stored."""

# Location of archived projects.
PROJECT_ARCHIVE = os.environ.get("PROJECT_ARCHIVE", os.path.join(PROJECT_HOME, ".archive"))
"""Where projects are archived. Additional scripts may be written to further display projects in this directory."""

# Location of projects on hold.
PROJECTS_ON_HOLD = os.environ.get("PROJECTS_ON_HOLD", os.path.join(PROJECT_HOME, ".hold"))
"""Where inactive projects are stored."""

# Support for source code repo meta data.
BITBUCKET_SCM = "bitbucket.org"
"""The domain for Bitbucket."""

GITHUB_SCM = "github.com"
"""The domain for GitHub."""

REPO_META_PATH = os.environ.get("REPO_META_PATH", os.path.join(PROJECT_HOME, ".repos"))
"""Meta data (``repo.ini`` files) are stored where by ``checkoutproject``."""

# License options for the lice command.
LICENSE_CHOICES = (
    "afl3",
    "agpl3",
    "apache",
    "bsd2",
    "bsd3",
    "cc0",
    "cc_by",
    "cc_by_nc",
    "cc_by_nc_nd",
    "cc_by_nc_sa",
    "cc_by_nd",
    "cc_by_sa",
    "cddl",
    "epl",
    "gpl2",
    "gpl3",
    "isc",
    "lgpl",
    "mit",
    "mpl",
    "wtfpl",
    "zlib",
)
"""License choices used by ``initproject``."""

# Bitbucket integration requires a user name and password.
BITBUCKET_USER = os.environ.get("BITBUCKET_USER", None)
"""The Bitbucket user name."""

BITBUCKET_PASSWORD = os.environ.get("BITBUCKET_PASSWORD", None)
"""The Bitbucket password for ``BITBUCKET_USER``."""

if BITBUCKET_USER and BITBUCKET_USER:
    BITBUCKET_ENABLED = True
    """Bitbucket is enabled if a user and password has been set."""
else:
    BITBUCKET_ENABLED = False

# GitHub integration is only possible if the user sets a user and password in the local environment.
GITHUB_USER = os.environ.get("GITHUB_USER", None)
"""The GitHub user name."""

GITHUB_PASSWORD = os.environ.get("GITHUB_PASSWORD", None)
"""The GitHub password for ``GITHUB_USER``."""

if GITHUB_USER and GITHUB_PASSWORD:
    GITHUB_ENABLED = True
    """GitHub is enabled if a user and password has been set."""
else:
    GITHUB_ENABLED = False

# The default SCM is the user's preferred provider (host) for repos.
DEFAULT_SCM = os.environ.get("DEFAULT_SCM", "github")
"""The default source code management tool to use for ``checkoutproject`` and other repo operations."""

# Control for links. The first value is the type as recognized by Project and the second is the Font Awesome icon
# to use for the link. See http://fontawesome.io/icons/
LINK_CATEGORIES = (
    ("chat", "comments"),
    ("deploy", "rocket"),
    ("docs", "book"),
    ("help", "question-circle"),
    ("home", "home"),
    ("issues", "bug"),
    ("project", "calendar"),
    ("roadmap", "map"),
    ("scm", "code-fork"),
)
"""Establish the recognized links and the icon to use when displayed as HTML."""
