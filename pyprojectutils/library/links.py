"""

.. versionadded:: 0.28.0-d

"""

# Imports

from .constants import LINK_CATEGORIES

# Exports

__all__ = (
    "AutoLink",
    "Link",
)

# Classes


class Link(object):
    """Represents a link, especially one associated with a project."""

    def __init__(self, url, category=None):
        """Initialize a link.

        :param url: The URL.
        :type url: str

        :param category: The link category. See ``LINK_CATEGORIES``.
        :type category: str

        """
        self.category = category
        self._url = url

    def get_icon(self):
        """Get the Font Awesome font key word to use for the link.

        :rtype str

        .. tip::
            This is here to allow overriding of how the icon is obtained.

        """
        for category, icon in LINK_CATEGORIES:
            if category == self.category:
                return icon

        return "link"

    def get_url(self):
        """Get the URL of the link.

        :rtype: str

        .. tip::
            This is here to allow overriding of how the URL is obtained.

        """
        return self._url

    @property
    def icon(self):
        """Alias of ``get_icon()``."""
        return self.get_icon()

    def to_html(self):
        """Get the link as HTML.

        :rtype: str

        """
        return '<a href="%s" title="%s"><i class="fa fa-%s" aria-hidden="true"></i></a>' % (
            self.url,
            self.category,
            self.icon
        )

    @property
    def url(self):
        """Alias of ``get_url()``."""
        return self.get_url()


class AutoLink(Link):
    """Incomplete example of how automatic links might work.

    .. code-block:: ini

        [urls]
        home = example.net
        bitbucket = %(BITBUCKET_USER)s
        codebasehq = develmaycare

    """

    def __init__(self, project, url, category=None):
        """Initialize an automatic link.

        :param project: The project instance.
        :type project: projects.Project

        :param url: The URL.
        :type url: str

        :param category: The link category.
        :type category: str

        """
        super(AutoLink, self).__init__(url, category=category)
        self.project = project

    def get_icon(self):
        # We can't do any guessing if no category was given.
        if self.category is None:
            return super(AutoLink, self).get_icon()

        # Lowercase the category, just in case.
        category = self.category.lower()

        # Get the icon based on category.
        if category == "bitbucket":
            return "bitbucket"
        elif category == "codebasehq":
            return "code"
        elif category == "doneonde":
            return "check"
        elif category == "fogbugz":
            return "bug"
        elif category == "github":
            return "github"
        elif category == "waffle":
            return "th"
        else:
            return super(AutoLink, self).get_icon()

    def get_url(self):
        """Get the URL for the link.

        :rtype: str

        """
        # If the URL begins with http, we'll return it as is. Otherwise, we'll try to create the URL automatically
        # based on the category.
        if self._url[:4] == "http":
            return self._url

        # We can't do any guessing if no category was given.
        if self.category is None:
            return self._url

        # Lowercase the category, just in case.
        category = self.category.lower()

        if category == "bitbucket":
            return "https://bitbucket.org/%s/%s" % (self.url, self.project)
        elif category == "codebasehq":
            # https://ptltd.codebasehq.com/projects/zoo-keeper/overview
            return "https://%s.codebasehq.com/projects/%s/overview" % (self.url, self.project.slug)
        elif category == "donedone":
            # https://kane.mydonedone.com/issuetracker/projects/55174
            if self.project.has_section("donedone"):
                return "https://%s.mydonedone.com/issuetracker/projects/%s" % (
                    self.project.donedone.subdomain,
                    self.project.donedone.project_id
                )
            else:
                return self._url
        elif category == "fogbugz":
            # https://ptltd.fogbugz.com/f/filters/4/Basis-HR-Application-Open
            return "https://%s.fogbugz.com/" % (
                self.url,
            )
        elif category == "github":
            return "https://github.com/%s/%s" % (self.url, self.project)
        elif category == "waffle":
            # https://waffle.io/develmaycare/pyprojectutils
            return "https://waffle.io/%s/%s" % (self.url, self.project)
        else:
            return self._url

    @property
    def url(self):
        return self.get_url()
