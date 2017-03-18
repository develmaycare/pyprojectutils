import os

__all__ = (
    "AUTHOR",
    "BASE_ENVIRONMENT",
    "BITBUCKET_SCM",
    "BUSINESS",
    "CLIENT",
    "CONTROL_ENVIRONMENT",
    "DEFAULT_SCM",
    "DEVELOPMENT",
    "DEVELOPMENT_ENVIRONMENT",
    "ENVIRONMENTS",
    "EXIT_ENV",
    "EXIT_INPUT",
    "EXIT_OK",
    "EXIT_OTHER",
    "EXIT_USAGE",
    "EXPERIMENTAL",
    "GITHUB_SCM",
    "LICENSE_CHOICES",
    "LINK_CATEGORIES",
    "LIVE",
    "LIVE_ENVIRONMENT",
    "PLANNING",
    "PUBLISHER",
    "RELEASE",
    "STAGING",
    "STAGING_ENVIRONMENT",
    "TESTING",
    "TESTING_ENVIRONMENT",
)

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

# Support for source code repo meta data.
BITBUCKET_SCM = "bitbucket.org"
"""The domain for Bitbucket."""

GITHUB_SCM = "github.com"
"""The domain for GitHub."""

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
    "private",
)
"""License choices used by ``initproject``."""

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
