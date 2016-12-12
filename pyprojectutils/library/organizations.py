"""
.. versionadded:: 0.16.0-d

Organizations represents the people involved in a project.

"""
# Imports

from .constants import BUSINESS, CLIENT

# Exports

__all__ = (
    "BaseOrganization",
    "Business",
    "Client",
)

# Classes


class BaseOrganization(object):
    """Base for organization classes."""

    def __init__(self, name, code=None, contact=None, projects=None):
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
