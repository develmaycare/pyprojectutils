# Imports

from config import Config, Section
from constants import BASE_ENVIRONMENT
from exceptions import OutputError

# Exports

__all__ = (
    "Apt",
    "BasePackage",
    "Brew",
    "Gem",
    "Npm",
    "PackageConfig",
    "Pip",
)

# Classes


class BasePackage(Section):
    """Base class for creating packages.

    A package is a section to be included in a requirements file.

    .. code-block:: ini

        [django]
        docs = http://docs.djangoproject.com
        env = base
        home = http://djangoproject.com
        note = We use this all the time.
        scm = http://github.com/django/django
        title = Django
        version = >=1.10

    """

    def __init__(self, name, **kwargs):
        super(BasePackage, self).__init__(name, **kwargs)

        self.branch = kwargs.get("branch", None)
        self.cmd = kwargs.get("cmd", None)
        self.docs = kwargs.get("docs", None)
        self.egg = kwargs.get("egg", None)
        self.env = kwargs.get("env", BASE_ENVIRONMENT).split(" ")
        self.home = kwargs.get("home", None)
        self.manager = kwargs.get("manager", "pip")
        self.name = name
        self.note = kwargs.get("note", None)
        self.scm = kwargs.get("scm", None)
        self.title = kwargs.get("title", name)
        self.version = kwargs.get("version", None)

    def __str__(self):
        return self.name

    def get_command(self):
        """Get the command to install the package from the console.

        :rtype: str

        """
        raise NotImplementedError()

    @property
    def has_links(self):
        if self.docs:
            return True
        elif self.home:
            return True
        elif self.scm:
            return True
        else:
            return False

    def to_markdown(self):
        a = list()

        # Hierarchy is File > Requirements > Environment > Package. This makes the package title a level 4 header which
        # doesn't display well, so we just use bold instead.
        a.append("**%s**" % self.title)
        a.append("")

        if self.note:
            a.append(self.note)
            a.append("")

        if len(self.env) > 1:
            a.append("Part of these environments: *%s*" % ", ".join(self.env))
        else:
            a.append("Part of the *%s* environment." % "".join(self.env))
        a.append("")

        # Example: [Link text](http://example.com/>)
        if self.has_links:
            a.append("Links:")
            a.append("")

            if self.home:
                a.append("- [Home](%s)" % self.home)

            if self.docs:
                a.append("- [Documentation](%s)" % self.docs)

            if self.scm:
                a.append("- [Source Code](%s)" % self.scm)

            a.append("")

        a.append("To install manually:")
        a.append("")
        a.append("    %s" % self.get_command())
        a.append("")

        return "\n".join(a)

    def to_plain(self):
        """Get the package output as a requirements file.

        :rtype: str

        """
        raise NotImplementedError()

    def to_rst(self):
        a = list()

        a.append(self.title)
        a.append("-" * len(self.title))
        a.append("")

        if self.note:
            a.append(self.note)
            a.append("")

        if len(self.env) > 1:
            a.append("Part of these environments: *%s*" % ", ".join(self.env))
        else:
            a.append("Part of the *%s* environment." % "".join(self.env))
        a.append("")

        # Example: `Link text <http://example.com/>`_
        if self.has_links:
            if self.home:
                a.append("- `Home <%s/>`_" % self.home)

            if self.docs:
                a.append("- `Documentation <%s/>`_" % self.docs)

            if self.scm:
                a.append("- `Source Code <%s/>`_" % self.scm)

            a.append("")

        a.append("To install manually:")
        a.append("")
        a.append(".. code-block:: bash")
        a.append("")
        a.append("    %s" % self.get_command())
        a.append("")

        return "\n".join(a)


class Apt(BasePackage):
    """An apt package."""

    def __init__(self, name, **kwargs):
        super(Apt, self).__init__(name, **kwargs)
        self.manager = "apt"

    def get_command(self):
        if self.cmd:
            return self.cmd

        cmd = "apt-get install -y"
        if self.version:
            cmd += " %s%s" % (self.name, self.version)
        else:
            cmd += " %s" % self.name

        return cmd

    def to_plain(self):
        return self.name


class Brew(BasePackage):
    """A Homebrew package."""

    def __init__(self, name, **kwargs):
        super(Brew, self).__init__(name, **kwargs)
        self.manager = "brew"

    def get_command(self):
        if self.cmd:
            return self.cmd

        cmd = "brew install %s" % self.name
        if self.version:
            cmd += self.version

        return cmd

    def to_plain(self):
        return self.name


class Gem(BasePackage):
    """A Gem package."""

    def __init__(self, name, **kwargs):
        super(Gem, self).__init__(name, **kwargs)
        self.manager = "gem"

    def get_command(self):
        if self.cmd:
            return self.cmd

        cmd = "gem install"
        if self.version:
            cmd += " --version %s %s" % (self.name, self.version)
        else:
            cmd += " %s" % self.name

        return cmd

    def to_plain(self):
        return self.name


class Npm(BasePackage):
    """A Npm package."""

    def __init__(self, name, **kwargs):
        super(Gem, self).__init__(name, **kwargs)
        self.manager = "npm"

    def get_command(self):
        if self.cmd:
            return self.cmd

        cmd = "npm install"
        if self.version:
            cmd += " %s@%s" % (self.name, self.version)
        else:
            cmd += " %s" % self.name

        return cmd

    def to_plain(self):
        return self.name


class Pip(BasePackage):
    """"A pip package."""

    def __init__(self, name, **kwargs):
        super(Pip, self).__init__(name, **kwargs)
        self.manager = "pip"

    def get_command(self):
        if self.cmd:
            return self.cmd

        cmd = "pip install"

        if self.egg:
            cmd += " %s" % self.to_plain()
        elif self.version:
            cmd += " %s%s" % (self.name, self.version)
        else:
            cmd += " %s" % self.name

        return cmd

    def to_plain(self):
        """Get the package output as a requirements file.

        :rtype: str

        Examples of requirements file install:

            django
            -e git+https://bitbucket.org/bogeymin/django-vanilla-viewsets/get/master.zip#egg=django-vanilla-viewsets
            -e git+https://github.com/bogeymin/django-htmgel.git#egg=htmgel
            -e git+https://github.com/bogeymin/tailfeathers.git@development#egg=tailfeathers

        """

        # Without an egg, we just return the package name.
        if not self.egg:
            return self.name

        # We can't go on without having the URL of the SCM.
        if not self.scm:
            raise OutputError("scm is required to use an egg with the %s package." % self.name)

        s = "-e"

        if "bitbucket" in self.scm:
            s += " git+%s/get/master.zip" % self.scm
        elif "github" in self.scm:
            if self.branch:
                s += " git+%s.git@%s" % (self.scm, self.branch)
            else:
                s += " git+%s.git" % self.scm
        else:
            pass

        s += "#egg=%s" % self.egg

        return s


class PackageConfig(Config):
    """A ``packages.ini`` file."""

    def __init__(self, path):
        super(PackageConfig, self).__init__(path)

    def get_packages(self, env=None, manager=None):
        """Get packages from this configuration.

        :param env: Optional environment name by which to filter packages.
        :type env: str

        :param manager: Optional package manager name by which to filter packages.
        :type manager: str

        :rtype: list

        """
        a = list()
        for section_name in self._sections:
            section = self.get_section(section_name)
            if env and env not in section.env:
                continue

            if manager and manager != section.manager:
                continue

            a.append(section)

        return a

    def _load_section(self, name, values):
        manager = values.get("manager", "pip")
        if manager == "apt":
            cls = Apt
        elif manager == "brew":
            cls = Brew
        elif manager == "gem":
            cls = Gem
        elif manager == "npm":
            cls = Npm
        else:
            cls = Pip

        section = cls(name, **values)
        setattr(self, name, section)
        self._sections.append(name)
        return section
