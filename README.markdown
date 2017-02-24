[![Stories in Ready](https://badge.waffle.io/develmaycare/pyprojectutils.png?label=ready&title=Ready)](https://waffle.io/develmaycare/pyprojectutils)
# Project Utils

A collection of documentation and command line utilities for managing a software project.

##  Status

This project is still under active development, but we're using it every day. It is reasonably stable if you want to
try it out, but things will be changing over time.

## Install

To install:

	pip install -e git+https://github.com/develmaycare/pyprojectutils.git#egg=pyprojectutils

You can decide whether this should be installed in a virtual environment or as part of the global environment. We
install it globally so it will work regardless of the active virtual env.

## Development

Set your ``$PROJECT_HOME``. If you use [Virtual Env Wrapper][virtualenvwrapper] (and you
should), then this is already done.

[virtualenvwrapper]: http://virtualenvwrapper.readthedocs.io/en/latest/

Download the source:

	cd $PROJECT_HOME;
	git clone git@github.com:bogeymin/pyprojectutils.git;
	
Install the requirements:

	pip install -r pyprojectutils/requirements.pip;
	
## The Commands

The commands included in this package are:

- archiveproject
- bumpversion
- checkoutproject
- enableproject
- exportgithub
- holdproject
- initproject
- lsdependencies
- lsdocumentation
- lsprojects
- lsrepos
- randompw
- statproject

See [the command reference](https://github.com/develmaycare/pyprojectutils/blob/master/docs/commands.rst).
