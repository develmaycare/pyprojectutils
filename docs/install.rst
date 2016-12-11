*******
Install
*******

This project is still under active development. To install:

.. code-block:: bash

	pip install -e git+https://github.com/bogeymin/pyprojectutils.git#egg=pyprojectutils;

You can decide whether this should be installed in a virtual environment or as part of the global environment. We
install it globally so it will work regardless of the active virtual env.

Environment Variables
=====================

``DEVELOPER_CODE``
------------------

Default: ``UNK`` (for *unknown*)

The developer code is merely a short form of the developer name, such as an abbreviation. For example, we abbreviate
*Devel May Care* as *DMC*.

``DEVELOPER_NAME``
------------------

Default: ``Unidentified``

The developer name is the name of the individual or company that creates and manages projects on the local machine. This
may be your name, or the name of your organization.

``PROJECT_HOME``
----------------

Default: ``~/Work``

This is borrowed from `Virtual Env Wrapper`_ and is the location of where projects are stored on your local machine.

.. note::
    User home is automatically expanded.

_Virtual Env Wrapper: http://virtualenvwrapper.readthedocs.io
