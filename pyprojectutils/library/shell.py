"""

.. versionadded:: 0.25.0-d

"""
# Imports

from subprocess import CalledProcessError, check_output

# Exports

__all__ = (
    "Command",
)

# Functions


class Command(object):
    """Represents a base shell command.,

    .. versionadded:: 0.27.0-d

    .. note::
        We are using ``shell=True`` to support piping and (possibly other) shell features. This is not advised due to
        security concerns, but all commands are processed internally without user input, so we feel the risk is low.
        See http://stackoverflow.com/a/13332300/241720

    """

    def __init__(self, string, path=None):
        """Prepare the command.

        :param string: The command to be executed.
        :type string: str

        :param path: The path from which the command should be executed.
        :type path: str

        """
        self.error = None
        self.output = None
        self.status = None
        self.string = string
        self._tokens = string.split(" ")

        if path:
            self.path = r'%s' % path
        else:
            self.path = None

    def preview(self):
        """Get a preview of the command.

        :rtype: str

        .. versionadded:: 0.34.4-d
            The preview shows what the command would be if executed manually, but the internals is still handled by
            subprocess, and in particular, the current working directory.

        """
        if self.path:
            return "(cd %s && %s)" % (self.path, self.string)
        else:
            return self.string

    def raw(self):
        """Run the command without exception handling. Useful for debugging."""
        self.output = check_output(self._tokens, cwd=self.path, shell=True)

    def run(self):
        """Run the command.

        :rtype: bool

        """
        try:
            self.output = check_output(self._tokens, cwd=self.path, shell=True)
            self.status = 0
            return True
        except CalledProcessError as e:
            self.error = e.message
            self.output = e.output
            self.status = e.returncode
            return False
