"""

.. versionadded:: 0.25.0-d

"""
# Imports

from shell_command import shell_output
import subprocess


# Functions


class Command(object):
    """Represents a base shell command.,

    .. versionadded:: 0.27.0-d

    """

    def __init__(self, string, path=None):
        """Prepare the command.

        :param string: The command to be executed.
        :type string: str

        :param path: The path from which the command should be executed.
        :type path: str

        """
        self.output = None
        self.path = path
        self.status = None
        self.string = string

    def raw(self):
        """Run the command without exception handling. Useful for debugging."""
        self.output = shell_output(self.string, cwd=self.path)

    def run(self):
        """Run the command."""

        try:
            self.output = shell_output(self.string, cwd=self.path)
            self.status = 0
            return True
        except subprocess.CalledProcessError as e:
            self.output = e.output
            self.status = e.returncode
            return False


def shell_command(command, path=None):
    """Get the status and output of a given command.

    :param command: The command to execute.
    :type command: str

    :rtype: list[int,str]
    :returns: Returns the exit code and output of the command as a list.

    """
    try:
        output = subprocess.check_output(command, cwd=path)
        return [0, output]
        tokens = command.split(" ")
        cmd = tokens.pop(0)
        args = " ".join(tokens)
        output = subprocess.check_output([cmd, args], cwd=path)
        return [0, output]
    except subprocess.CalledProcessError as error:
        return [error.returncode, error.output]
