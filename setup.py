# See https://packaging.python.org/en/latest/distributing.html
# and https://docs.python.org/2/distutils/setupscript.html
# and https://pypi.python.org/pypi?%3Aaction=list_classifiers

from os.path import join, exists as path_exists
from setuptools import setup, find_packages


def read_file(path):
    with open(path, "rb") as f:
        contents = f.read()
        f.close()
    return contents


def get_description():

    files = ("README", "COPYING", "CHANGES", "TODO")
    extensions = ("markdown", "md", "rst", "txt")

    description = ""
    for file_name in files:
        for ext in extensions:
            path = "%s.%s" % (file_name, ext)
            if path_exists(path):
                description += read_file(path)

    return description


def get_version():
    return read_file("VERSION.txt")


setup(
    name='pyprojectutils',
    version=get_version(),
    description='A collection of documentation and command line utilities for managing a software project.',
    long_description=get_description(),
    author='Shawn Davis',
    author_email='shawn@ptltd.co',
    url='https://github.com/bogeymin/pyprojectutils',
    packages=find_packages(),
    install_requires=[
        "semver",
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
    zip_safe=False,
    tests_require=[
        "semver",
    ],
    test_suite='runtests.runtests',
    entry_points={
      'console_scripts': [
          'lspackages = pyprojectutils.cli:package_parser',
          'lsprojects = pyprojectutils.cli:project_parser',
          'randompw = pyprojectutils.cli:generate_password',
          'versionbump = pyprojectutils.cli:version_update',
      ],
    },
)
