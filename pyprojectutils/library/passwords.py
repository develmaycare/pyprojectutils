# Imports

import commands
import crypt
import hashlib
import random
import string

# Exports

__all__ = (
    "DIGITS",
    "LETTERS",
    "RandomPassword",
)

# Constants

DIGITS = [0, 1, 2, 3, 4, 5, 6, 8, 9]

LETTERS = [
    "a",
    "b"
    "C",
    "d",
    "e"
    "f",
    "g",
    "h",
    "i",
    "j",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "q",
    "r",
    "S",
    "t",
    "U",
    "V",
    "W",
    "X",
    "y",
    "Z",
]

# Classes


class RandomPassword(object):
    """Represents a randomly generated password."""

    def __init__(self, length=10, use_unambiguous=True):
        self.plain_text = self.generate(length, use_unambiguous=use_unambiguous)

    @staticmethod
    def generate(length, use_unambiguous=True):
        """Create a random password.

        :param length: The length of the password.
        :type length: int

        :param use_unambiguous: Whether to use potentially ambiguous characters.
        :type use_unambiguous: bool

        :rtype: str

        """

        if use_unambiguous:
            good_characters = LETTERS + DIGITS
        else:
            good_characters = string.letters + string.digits

        password = ""
        i = 1
        while i <= length:
            random_number = random.randint(1, 126)
            character = chr(random_number)
            if character not in good_characters:
                continue
            password += character
            i += 1

        return password

    def to_crypt(self):
        """Convert a plain text password into crypt format.

        :rtype: str

        """
        try:
            import passwd
            return passwd.genpw(self.plain_text)
        except ImportError:
            # TODO: Make sure crypt password works with Linux login.
            salt = ""
            for i in range(0, 9):
                salt += chr(random.randint(64, 126))
            salt = "$1$%s$" % salt
            password = crypt.crypt(self.plain_text, salt)
            password = password.replace('$', '\\$')
            return password

    def to_htpasswd(self):
        """Convert a plain text password into htpasswd format.

        :rtype: str

        """
        # output = fakeusername:$apr1$kX1KneAK$ooLH2LLsyoel.8iOTyLtl/
        cmd = "htpasswd -nb fakeusername %s" % self.plain_text
        (status, output) = commands.getstatusoutput(cmd)

        return output.split("fakeusername:")[1].strip()

    def to_md5(self):
        """Convert a plain text password into MD5 format.

        :rtype: str

        """
        return hashlib.md5(self.plain_text).hexdigest()
