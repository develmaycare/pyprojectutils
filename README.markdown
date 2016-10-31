# Project Utils

A collection of documentation and command line utilities for managing a software project.

## Install

Download the source:

	git clone git@github.com:bogeymin/project-utils.git;
	
Set your ``$PROJECT_HOME``. If you use [Virtual Env Wrapper][virtualenvwrapp] (and you
should), then this is already done.

[virtualenvwrapp]: http://virtualenvwrapper.readthedocs.io/en/latest/
	
Install the requirements:

	pip install -r project-utils/requirements.pip;
	
Copy the commands to your executable path. For example:

	cp project-utils/bin/lsprojects.py /usr/local/bin/lsprojects;
	cp project-utils/bin/randompw.py /usr/local/bin/randompw;
	cp project-utils/bin/versionbump.py /usr/local/bin/versionbump;

## The Commands

### lsprojects

List and filter projects in the projects directory.

	usage: lsprojects.py [-h] [-a] [-c= CLIENT_CODE] [--dirty] [-d]
						 [-n= PROJECT_NAME] [-p= PROJECT_HOME] [-s= STATUS]
						 [-t= PROJECT_TYPE] [-v] [--version]

	List and filter projects in the projects directory.

	optional arguments:
	  -h, --help            show this help message and exit
	  -a, --all             Show projects even if there is no project.ini
	  -c= CLIENT_CODE, --client= CLIENT_CODE
							Filter by client organization. Use ? to list
							organizations
	  --dirty               Only show projects with dirty repos
	  -d, --disk            Calculate disk space. Takes longer to run.
	  -n= PROJECT_NAME, --name= PROJECT_NAME
							Find a project by name and display it's information.
	  -p= PROJECT_HOME, --path= PROJECT_HOME
							Path to where projects are stored. Defaults to
							/Users/shawn/Work
	  -s= STATUS, --status= STATUS
							Filter by project status. Use ? to list available
							statuses.
	  -t= PROJECT_TYPE, --type= PROJECT_TYPE
							Filter by project type. Use ? to list available types.
	  -v                    Show version number and exit.
	  --version             Show verbose version information and exit.

#### Format of INI

You can provide a ``project.ini`` file to provide detail on the project that
cannot be gleaned from the file system.

    [project]
    description = A description of the project.
    scope = website
    status = development
    tags = CRM, Sales
    type = django
    title = Project Title

    [business]
    code = PTL
    name = Pleasant Tents, LLC

    [client]
    code = ACME
    name = ACME, Inc

    [domain]
    name = example
    tld = com

The ``tags``, ``type``, ``scope``, and ``status`` may be whatever you like.

#### Sections

Attributes of ``[project]`` section are used as is. ``[business]`` ``[client]``
are used to identify the beneficiary and/or developer of the project.

Other sections may be added as you see fit.

#### Additional Data

Additional data may be displayed in the list output and when using the
``--name`` switch.

- The SCM and disk usage of the project may be automatically determined.
- The project tree is obtained with the ``tree`` command.

#### Generating a README

The ``--name`` switch searches for a specific project and (if found) outputs
project information in [Markdown][markdown] format:

[markdown]: http://daringfireball.net/projects/markdown/

    cd example_project;
    lsprojects --name=example_project > README.markdown;

Although you'll likely want to customize the output, this is handy for
creating (or recreating) a README for the project.

### randompw

Generate a random password.

	usage: randompw.py [-h] [--format= [{crypt,md5,plain,htpasswd}]] [--strong]
					   [-U]

	Generate a random password.

	optional arguments:
	  -h, --help            show this help message and exit
	  --format= [{crypt,md5,plain,htpasswd}]
							Choose the format of the output.
	  --strong              Make the password stronger.
	  -U                    Avoid ambiguous characters.

We often need to generate passwords automatically. This utility does just
that. Upload it during deployment to create passwords on the fly.

### versionbump

Increment the version number immediately after checking out a release branch.

	usage: versionbump.py [-h] [-b= BUILD] [--force] [-M] [-m] [-n= NAME] [-p]
						  [-P= PATH] [--preview] [-s= STATUS] [-T= TEMPLATE] [-v]
						  [--version]
						  project_name [string]

	Increment the version number immediately after checking out a release branch.

	positional arguments:
	  project_name          The name of the project. Typically, the directory name
							in which the project is stored.
	  string                The specific release string to assign.

	optional arguments:
	  -h, --help            show this help message and exit
	  -b= BUILD, --build= BUILD
							Supply build meta data.
	  --force               By default, setting the major version resets minor and
							patch to 0, and setting minor resets patch to 0. Use
							this switch to force the exact version that you
							specify.
	  -M, --major           Increase the major version number when you make
							changes to the public API that are backward-
							incompatible.
	  -m, --minor           Increase the minor version number when new or updated
							functionality has been implemented that does not
							change the public API.
	  -n= NAME, --name= NAME
							Name your release.
	  -p, --patch           Set (or increase) the patch level when backward-
							compatible bug-fixes have been implemented.
	  -P= PATH, --path= PATH
							The path to where projects are stored. Defaults to
							/Users/shawn/Work
	  --preview             Preview the output, but don't make any changes.
	  -s= STATUS, --status= STATUS
							Use the status to denote a pre-release version.
	  -T= TEMPLATE, --template= TEMPLATE
							Path to the version.py template you would like to use.
							Use ? to see the default.
	  -v                    Show version number and exit.
	  --version             Show verbose version information and exit.

#### When to Use

Generally, you want to increment the version number immediately after checking
out a release branch. However, you may wish to bump the version any time
during development, especially during early development where the MINOR
and PATCH versions are changing frequently.

Here is an example workflow:

    # Get the current version and check out the next release.
    versionbump myproject; # get the current version, example 1.2
    git checkout -b release-1.3;

    # Bump automatically sets the next minor version with a status of d.
    versionbump myproject -m -s d;

    # Commit the bump.
    git commit -am "Version Bump";

    # Go do the final work for the release.
    # ...

    # Merge the release.
    git checkout master;
    git merge --no-ff release-1.3;
    git tag -a 1.3;

    # Merge back to development.
    git checkout development;
    git merge --no-ff release-1.3;

#### Semantic Versioning

This utility makes use of [Semantic Versioning](semver.org). From the
documentation:

1. MAJOR version when you make incompatible API changes,
2. MINOR version when you add functionality in a backwards-compatible manner,
   and
3. PATCH version when you make backwards-compatible bug fixes.

Additional labels for pre-release and build metadata are available as
extensions to the MAJOR.MINOR.PATCH format.

**Status**

We define the following status codes:

- x - Prototype, experimental. Use at your own risk.
- d - Development. Unstable, untested.
- a - Feature complete.
- b - Ready for testing and QA.
- r - Release candidate.
- o - Obsolete, deprecated, or defect. End of life.

You may of course use whatever status you like.

#### Release Versus Version

**Release**

A *release* is a collection of updates representing a new version of the
product. A release is represented by the full string of MAJOR.MINOR.PATCH,
and may optionally include the status and build until the release is live.

The release is probably never displayed to Customers or Users.

**Version**

A *version* represents a specific state of the product. The version is
represented by the MAJOR.MINOR string of the release.

The version may be shown to Customers or Users.
