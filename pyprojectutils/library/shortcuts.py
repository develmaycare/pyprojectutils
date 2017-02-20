# Imports

import os
from string import Template
import sys
from .colors import blue, green, red, yellow
from .exceptions import OutputError

# Exports

__all__ = (
    "bool_to_yes_no",
    "debug",
    "find_file",
    "get_input",
    "make_dir",
    "parse_template",
    "print_error",
    "print_info",
    "print_success",
    "print_warning",
    "read_file",
    "write_file",
)

# Functions


def bool_to_yes_no(value):
    """Convert a boolean (or ``None``) to a yes/no string.

    :param value: The value to be converted.
    :type value: bool

    :rtype: str

    .. versionadded:: 0.27.0-d

    """
    if value is True:
        return "yes"
    else:
        return "no"


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


def find_file(name, path):
    """Find a file relative to a given path.

    :param name: The file name.
    :type name: str

    :param path: The path to check. The function looks up to two directories above the given path.
    :type path: str

    :rtype: str || None
    :returns: The full file path or ``None`` if the file could not be found.

    .. versionadded:: 0.17.0-d

    """
    # Assemble the possible locations for the file.
    locations = (
        os.path.join(path, name),
        os.path.abspath(os.path.join(path, "../", name)),
        os.path.abspath(os.path.join(path, "../../", name)),
    )
    # print(locations)

    for location in locations:
        if os.path.exists(location):
            return location

    return None


def get_input(label, choices=None, default=None, required=False):
    """Wraps ``raw_input()`` to add choices, default and required options.

    :param label: The label to be displayed as the prompt.
    :type label: str

    :param choices: List of valid choices, if any.
    :type choices: list[str]

    :param default: Default value if nothing is entered.
    :type default: str | None

    :param required: Indicates input is required.
    :type required: bool

    .. versionadded:: 0.16.0-d

    .. note::
        A space at the end of the label is added automatically. A colon is also added.

    """

    if choices:
        if required:
            label = "%s (required)"

        print(label)

        for c in choices:
            if c == default:
                print("    %s (default)" % c)
            else:
                print("    %s" % c)
        print("")

        value = raw_input("Your choice: ")
    else:
        if default:
            label = "%s [%s]" % (label, default)

        if required:
            label += " (required)"

        label += ": "

        value = raw_input(label)

    if not value:

        if default:
            return default

        if required:
            return get_input(label, choices=choices, default=default, required=required)

    return value


def make_dir(path):
    """Create a directory if it does not already exist.

    :param path: The path to the directory.
    :type path: str

    :rtype: bool
    :returns: Returns ``True`` if the directory already exists.

    .. versionadded: 0.18.0-d

    """
    print path

    if os.path.exists(path):
        return True

    os.makedirs(path)
    return False


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


def print_error(message, exit_code=None):
    """Print an error message.

    :param message: The message to be displayed.
    :type message: str

    :param exit_code: The exit code, if given, will cause the script to terminate. See ``constants.py``.
    :type exit_code: int

    .. versionadded:: 0.16.0-d

    """
    print(red(message))

    if exit_code:
        sys.exit(exit_code)


def print_info(message, exit_code=None):
    """Print an informational message.

    :param message: The message to be displayed.
    :type message: str

    :param exit_code: The exit code, if given, will cause the script to terminate. See ``constants.py``.
    :type exit_code: int

    .. versionadded:: 0.16.0-d

    .. versionchanged:: 0.18.0-d
        Added ``exit_code`` parameter.

    """
    print(blue(message))

    if exit_code:
        sys.exit(exit_code)


def print_success(message, exit_code=None):
    """Print a success message.

    :param message: The message to be displayed.
    :type message: str

    :param exit_code: The exit code, if given, will cause the script to terminate. See ``constants.py``.
    :type exit_code: int

    .. versionadded:: 0.16.0-d

    .. versionchanged:: 0.18.0-d
        Added ``exit_code`` parameter.

    """
    print(green(message))

    if exit_code:
        sys.exit(exit_code)


def print_warning(message, exit_code=None):
    """Print a warning message.

    :param message: The message to be displayed.
    :type message: str

    :param exit_code: The exit code, if given, will cause the script to terminate. See ``constants.py``.
    :type exit_code: int

    .. versionadded:: 0.16.0-d

    .. versionchanged:: 0.18.0-d
        Added ``exit_code`` parameter.

    """
    print(yellow(message))

    if exit_code:
        sys.exit(exit_code)


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
