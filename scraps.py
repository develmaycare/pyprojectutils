    # Initialize a project instance.
    project = Project(project_name, project_root)

    # Initialize upon request.
    if args.initialize:
        if args.preview_only:
            print("Initialization does not support preview.")
            sys.exit(EXIT_USAGE)

        files = project.initialize()

        print("\n".join(files))
        print("Initialized %s files" % len(files))

        sys.exit(EXIT_OK)

class Project(object):
    """Represents the version (and release) of a project."""

    def __init__(self, name, root=None):
        self.name = name
        self.next_version = None
        self.root = root or os.path.join(PROJECT_HOME, name)
        self.version_py = None
        self.version_txt = os.path.join(self.root, "VERSION.txt")

        if self.has_version_txt:
            self.current_version = Version(read_file(self.version_txt))
        else:
            self.current_version = Version("0.1.0-d")

        for p in VERSION_PY_LOCATIONS:
            version_py = p % {'project_name': name, 'project_root': self.root}
            if os.path.exists(version_py):
                self.version_py = version_py
                break

    def bump_major(self):
        """Increase the major version."""
        self.next_version = Version(semver.bump_major(self.current_version.string))

    def bump_minor(self):
        """Increase the minor version."""
        self.next_version = Version(semver.bump_minor(self.current_version.string))

    def bump_patch(self):
        """Increase the patch level."""
        self.next_version = Version(semver.bump_patch(self.current_version.string))

    def get_version(self):

    @property
    def has_version_py(self):
        if self.version_py is None:
            return False

        return os.path.exists(self.version_py)

    @property
    def has_version_txt(self):
        return os.path.exists(self.version_txt)

    def initialize(self):
        """Initialize version files with the default version."""
        files = list()

        # Create the VERSION.txt file.
        if not self.has_version_txt:
            write_file(self.version_txt, self.current_version)
            files.append(self.version_txt)

        # Create the version.py file.
        tokens = self.get_tokens()
        for i in VERSION_PY_LOCATIONS:
            version_py = i % {'project_name': self.name, 'project_root': self.root}
            if os.path.exists(os.path.dirname(version_py)):
                template = Template(TEMPLATE)
                content = template.substitute(**tokens)

                write_file(version_py, content)

                files.append(version_py)
                break

        return files

    def set_build(self, build):
        """Set the build number of the project version.

        :param build: The build number.
        :type build: str

        """
        if not self.next_version:
            self.next_version = Version(self.current_version.string)

        self.next_version.build = build

    def set_status(self, status):
        """Set the status (prerelease) of the project version.

        :param status: The status code.
        :type status: str

        """
        if not self.next_version:
            self.next_version = Version(self.current_version.string)

        self.next_version.status = status


class Version(object):
    """Represents a project version or release."""

    def __init__(self, string):
        self.object = semver.parse_version_info(string)
        self.string = string

        # Preserve the previous build and prereleast data.
        self.build_number = self.object.build
        self.status = self.object.prerelease

    @property
    def build(self):
        return self.object.build

    def bump_major(self):
        """Increase the major version."""
        return Version(semver.bump_major(self.string))

    def bump_minor(self):
        """Increase the minor version."""
        return Version
        self.current = semver.bump_minor(self.original)

    def bump_patch(self):
        """Increase the patch level."""
        self.current = semver.bump_patch(self.original)

    def get_tokens(self):
        """Get the version as a dictionary.

        :rtype: dict

        """
        if self.current:
            string = self.current
        else:
            string = self.original

        tokens = semver.parse(string)

        tokens['name'] = ""
        tokens['now'] = NOW

        if tokens['build'] is None:
            tokens['build'] = ""

        if tokens['prerelease'] is None:
            tokens['prerelease'] = ""

        return tokens

    @property
    def major(self):
        return self.object.major

    @property
    def minor(self):
        return self.object.minor

    @property
    def patch(self):
        return self.object.patch

    @property
    def prerelease(self):
        return self.object.prerelease

    def to_string(self):
        """Get the version as a string.

        :rtype: str

        """

        return self.current or self.original