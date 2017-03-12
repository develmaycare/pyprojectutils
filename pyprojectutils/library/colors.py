"""
.. versionadded:: 0.16.0-d

Allows color to be added to command output. Set the ``PYROJECTUTILS_DISABLE_COLORS`` environment variable to disable
color even when color is requested.

.. note::
    This was copied from ``fabric/fabric/colors.py`` with just minor modifications.

"""
import os


def _wrap_with(code):

    def inner(text, bold=False):
        c = code

        if os.environ.get('PYROJECTUTILS_DISABLE_COLORS'):
            return text

        if bold:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)
    return inner

red = _wrap_with('31')
green = _wrap_with('32')
yellow = _wrap_with('33')
blue = _wrap_with('34')
magenta = _wrap_with('35')
cyan = _wrap_with('36')
white = _wrap_with('37')
