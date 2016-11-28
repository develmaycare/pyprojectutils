# Imports

import os
from string import Template

from exceptions import OutputError

# Functions


def debug(location, message, line=None):
    """Print a debug message.

    :param location: The location of the debug statement. Tip: Use ``__file__`` for the current file.
    :type location: str

    :param message: The message to print.
    :type message: str

    :param message: The line number.
    :type line: int

    """
    if line:
        output = "%s. [%s] %s" % (line, location, message)
    else:
        output = "[%s] %s" % (location, message)

    print(output)


def parse_template(context, template):
    """

    :param context: The context to be parsed into the string template.
    :type context: dict

    :param template: A string or path to use as the template.
    :type template: str

    :rtype: str

    """
    if os.path.exists(template):
        content = Template(read_file(template))
    else:
        content = Template(template)

    return content.substitute(**context)


def read_file(path):
    """Get the contents of a file in a memory-safe way.

    :param path: The file to read.
    :type path: str

    :rtype: str

    """
    try:
        with open(path, "rb") as f:
            content = f.read()
            f.close()

        return content
    except IOError:
        return ""


def write_file(path, content):
    """Write to a file in a memory-safe way.

    :param path: Path to the file.
    :type path: str

    :param content: Content of the file.
    :type content: str

    :rtype: bool
    :returns: ``True`` if the file could be written.

    """
    try:
        with open(path, "wb") as f:
            f.write(content)
            f.close()
        return True
    except IOError, e:
        raise OutputError(e)
