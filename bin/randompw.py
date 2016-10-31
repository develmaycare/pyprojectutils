#! /usr/bin/env python

# Imports

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import crypt
import hashlib
import os
import random
import string
import sys

# Administrivia

__author__ = "Shawn Davis <shawn@ptltd.co>"
__command__ = os.path.basename(sys.argv[0])
__date__ = "2015-10-31"
__version__ = "0.9.2-d"

# Constants

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_INPUT = 2
EXIT_ENV = 3
EXIT_OTHER = 4

DIGITS = [0, 1, 2, 3, 4, 5, 6, 8, 9]

HELP = """
We often need to generate passwords automatically. This utility does just
that. Upload it during deployment to create passwords on the fly.

"""

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

# Functions


def main():
    """Generate a random password."""

    description = main.__doc__

    # Define options and arguments.
    parser = ArgumentParser(description=description, epilog=HELP, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument(
        "--format=",
        choices=["crypt", "md5", "plain", "htpasswd"],
        default="plain",
        dest="format",
        help="Choose the format of the output.",
        nargs="?"
    )
    parser.add_argument("--strong", action="store_true", help="Make the password stronger.")
    parser.add_argument(
        "-U",
        action="store_true",
        dest="use_unambiguous",
        help="Avoid ambiguous characters."
    )

    # This will display help or input errors as needed.
    args = parser.parse_args()
    # print args

    password_length = 10
    if args.strong:
        password_length = 20

    password = get_random_password(password_length, args.use_unambiguous)

    if args.format == "crypt":
        try:
            import passwd
            print passwd.genpw(password)
        except ImportError:
            print get_crypt_password(password)
    elif args.format == "htpasswd":
        raise NotImplementedError()
    elif args.format == "md5":
        # TODO: Make sure md5 password works as a login.
        print hashlib.md5(password).hexdigest()
    else:
        print password

    # Quit.
    sys.exit(EXIT_OK)


def get_crypt_password(plain_text):
    # TODO: Make sure crypt password works with Linux login.
    salt = ""
    for i in range(0, 9):
        salt += chr(random.randint(64, 126))
    salt = "$1$%s$" % salt
    password = crypt.crypt(plain_text, salt)
    password = password.replace('$', '\\$')
    return password


def get_random_password(length, use_unambiguous=True):

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

# Kickoff
if __name__ == "__main__":
    main()
