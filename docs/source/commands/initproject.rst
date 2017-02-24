initproject
===========

Initialize a project, creating various common files using intelligent defaults. Or at least *some* defaults.

.. code-block:: none

    usage: initproject [-h] [-b= BUSINESS_NAME] [-B= BUSINESS_CODE]
                       [-c= CATEGORY] [--client= CLIENT_NAME]
                       [--client-code= CLIENT_CODE] [-d= DESCRIPTION]
                       [-L= LICENSE_CODE] [-p= PROJECT_HOME] [--prompt=]
                       [-s= STATUS] [--title= TITLE] [-t= PROJECT_TYPE] [-v]
                       [--version]
                       project_name

    positional arguments:
      project_name          The name of the project. The directory will be created
                            if it does not exist in $PROJECT_HOME

    optional arguments:
      -h, --help            show this help message and exit
      -b= BUSINESS_NAME, --business= BUSINESS_NAME
                            Set the name of the developer organization.
      -B= BUSINESS_CODE     Business code. If omitted it is automatically dervied
                            from the business name.
      -c= CATEGORY, --category= CATEGORY
                            Project category. For example, django or wagtail.
                            Default is "uncategorized".
      --client= CLIENT_NAME
                            Set the name of the client organization.
      --client-code= CLIENT_CODE
                            Client code. If ommited it is automatically dervied
                            from the client name.
      -d= DESCRIPTION, --description= DESCRIPTION
                            A brief description of the project.
      -L= LICENSE_CODE, --license= LICENSE_CODE
                            License code. Use lice --help for list of valid codes.
      -p= PROJECT_HOME, --path= PROJECT_HOME
                            Path to where projects are stored. Defaults to
                            ~/Work
      --prompt=             Prompt for options rather than providing them via the
                            command line.
      -s= STATUS, --status= STATUS
                            Filter by project status. Use ? to list available
                            statuses.
      --title= TITLE        Specify the project title. Defaults to the project
                            name.
      -t= PROJECT_TYPE, --type= PROJECT_TYPE
                            Specify the project type. Defaults to "project".
      -v                    Show version number and exit.
      --version             Show verbose version information and exit.
