[![Stories in Ready](https://badge.waffle.io/develmaycare/pyprojectutils.png?label=ready&title=Ready)](https://waffle.io/develmaycare/pyprojectutils)
# Project Utils

A collection of documentation and command line utilities for managing a software project.

## Install

To install:

	pip install -e git+https://github.com/bogeymin/pyprojectutils.git#egg=pyprojectutils

## Development

Set your ``$PROJECT_HOME``. If you use [Virtual Env Wrapper][virtualenvwrapp] (and you
should), then this is already done.

[virtualenvwrapp]: http://virtualenvwrapper.readthedocs.io/en/latest/

Download the source:

	cd $PROJECT_HOME;
	git clone git@github.com:bogeymin/pyprojectutils.git;
	
Install the requirements:

	pip install -r pyprojectutils/requirements.pip;
	
## The Commands

See [the command reference](https://github.com/develmaycare/pyprojectutils/blob/master/docs/commands.rst).

- bumpversion
- checkoutproject
- holdproject
- initproject
- lsdependencies
- lsprojects
- randompw

## Cookiecutter Templates

You may find these [Cookiecutter](http://cookiecutter.readthedocs.io/en/latest/) templates useful.

- [Ansible for Django](https://github.com/develmaycare/cookiecutter-ansible-django): Add a deploy directory to your Django project.
- [Django App (Full)](https://github.com/develmaycare/cookiecutter-django-app-full): A Django app with all of the tri- [Django App (Full)](https://github.com/develmaycare/cookiecutter-django-app-full): A Django app with all of the trimmings.
- [Static Website](https://github.com/develmaycare/cookiecutter-static-website): A simple static website.
