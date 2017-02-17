"""

.. versionadded:: 0.25.0-d

"""
# Imports

import subprocess


# Functions


def shell_command(command):
    """Get the status and output of a given command.

    :param command: The command to execute.
    :type command: str

    :rtype: list[int,str]
    :returns: Returns the exit code and output of the command as a list.

    """
    try:
        cmd = command.split(" ")
        output = subprocess.check_output(cmd)
        return [0, output]
    except subprocess.CalledProcessError as error:
        return [error.returncode, error.output]
