# Exports

__all__ = (
    "CommandFailed",
    "InputError",
    "OutputError",
    "ResourceUnavailable",
)

# Classes


class CommandFailed(Exception):
    """Occurs when a library function or method fails to successfully run a :py:class:`shell.Command`."""
    pass


class InputError(Exception):
    """Occurs when improper or invalid input has been supplied from a command to a library function or class."""
    pass


class OutputError(Exception):
    """Occurs when output cannot be generated."""
    pass


class ResourceUnavailable(Exception):
    """Occurs when a library function, method, or class is unable to import or use an external resource."""
    pass
