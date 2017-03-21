randompassword
==============

Generate a random password.

.. code-block:: none

    usage: randompassword [-h] [--format= [{crypt,md5,plain,htpasswd}]] [--strong]
                          [-U] [-v] [--version]

    optional arguments:
      -h, --help            show this help message and exit
      --format= [{crypt,md5,plain,htpasswd}]
                            Choose the format of the output.
      --strong              Make the password stronger.
      -U                    Avoid ambiguous characters.
      -v                    Show version number and exit.
      --version             Show verbose version information and exit.

We often need to generate passwords automatically. This utility does just
that. Install pyprojectutils during deployment to create passwords on the fly.

.. versionchanged:: 0.34.0-d
    Renamed from ``randompw`` to ``randompassword``.
