"""
.. versionadded:: 0.16.0-d

Organizations represents the people involved in a project.

"""
# Imports

from .config import Section
from .constants import BUSINESS, CLIENT

# Exports

__all__ = (
    "BaseOrganization",
    "Business",
    "Client",
)

# Classes


class BaseOrganization(Section):
    """Base for organization classes."""

    def __init__(self, name, code=None, contact=None, projects=None, **kwargs):
        """Initialize an organization.

        :param name: Name of the organization.
        :type name: str

        :param code: Abbreviation or code for the organization.
        :type code: str

        :param contact: Name of the contact at the organization.
        :type contact: str

        :param projects: A list of projects associated with the organization.
        :type projects: list[Project]

        .. versionchanged:: 0.28.0-d
            ``BaseOrganization`` now inherits from :py:class`config.Section`. Also added kwargs (which are currently
            ignored) so we can use ``SafeConfigParser`` without error.

        """
        self.code = code or self.get_default_code(name)
        self.contact = contact
        self.name = name
        self.projects = projects or list()

    @staticmethod
    def get_default_code(name):
        """Get the default organization code from the name.

        :param name: Name of the organization.
        :type name: str

        :rtype: str
        :returns: Returns a code for the organization by capitalizing the first letter of each word in the organization
                  name.

        """
        code = ""
        for i in name.split(" "):
            code += i[0].upper()

        return code

    def get_type(self):
        """Get the type of organization.

        :rtype: str

        """
        raise NotImplementedError()

    @property
    def type(self):
        """Alias of ``get_type()``."""
        return self.get_type()


class Business(BaseOrganization):
    """A business creates and manages projects on behalf of itself or a client."""

    def get_type(self):
        return BUSINESS


class Client(BaseOrganization):
    """A client is the benefactor of a project."""

    def get_type(self):
        return CLIENT
