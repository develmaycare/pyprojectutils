# See https://packaging.python.org/en/latest/distributing.html
# and https://docs.python.org/2/distutils/setupscript.html
# and https://pypi.python.org/pypi?%3Aaction=list_classifiers
from setuptools import setup, find_packages


def read(path):
    with open(path, "rb") as f:
        contents = f.read()
        f.close()
    return contents

setup(
    name='pyprojectutils',
    version=read("VERSION.txt"),
    description=read("DESCRIPTION.txt"),
    long_description=read("README.markdown"),
    author='Shawn Davis',
    author_email='shawn@develmaycare.com',
    url='https://github.com/develmaycare/pyprojectutils',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "gitpython",
        "jinja2",
        "semver",
    ],
    dependency_links=[
        "https://github.com/develmaycare/python-datetime-machine.git",
        "https://github.com/PyGithub/PyGithub.git",
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
        "gitpython",
        "jinja2",
        "semver",
    ],
    test_suite='runtests.runtests',
    entry_points={
      'console_scripts': [
          'archiveproject = pyprojectutils.cli:archive_project_command',
          'bumpversion = pyprojectutils.cli:bump_version_command',
          'checkoutproject = pyprojectutils.cli:checkout_project_command',
          'createrepo = pyprojectutils.cli:create_repo_command',
          'enableproject = pyprojectutils.cli:enable_project_command',
          'exportgithub = pyprojectutils.cli:export_github_command',
          'holdproject = pyprojectutils.cli:hold_project_command',
          'initproject = pyprojectutils.cli:init_project_command',
          'lsdependencies = pyprojectutils.cli:list_dependencies_command',
          'lsdocumentation = pyprojectutils.cli:list_documentation_command',
          'lsprojects = pyprojectutils.cli:list_projects_command',
          'lsrepos = pyprojectutils.cli:list_repos_command',
          'loremimage = pyprojectutils.cli:lorem_image_command',
          'loremtext = pyprojectutils.cli:lorem_text_command',
          'projecthelp = pyprojectutils.cli:project_help_command',
          'randompassword = pyprojectutils.cli:random_password_command',
          'statdocumentation = pyprojectutils.cli:stat_documentation_command',
          'statproject = pyprojectutils.cli:stat_project_command',
      ],
    },
)
