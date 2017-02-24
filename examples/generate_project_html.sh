#!/usr/bin/env bash

#! /bin/bash

###################################
# Functions
###################################

# TBD

###################################
# Configuration
###################################

# Script information.
AUTHOR="Shawn Davis <shawn@develmaycare.com>";
SCRIPT=`basename $0`;
DATE="2017-02-23";
VERSION="0.2.2-d";

# Exit codes.
EXIT_NORMAL=0;
EXIT_USAGE=1;
EXIT_ENVIRONMENT=2;
EXIT_OTHER=3;

# Map truth.
TRUE=0;
FALSE=1;

# Default output file.
OUTPUT_FILE=~/Work/projects.html;

# Temporary file.
#TEMP_FILE="/tmp/$SCRIPT".$$

###################################
# Help
###################################

HELP="
SUMMARY

Generate HTML version of the project list, including projects on hold and archived.

OPTIONS

-p <path>
    The output path. Defaults to $OUTPUT_FILE

-h
    Print help and exit.

--help
    Print more help and exit.

-v
    Print version and exit.

--version
    Print full version and exit.

NOTES

This is an example of how to use lsprojects with the HTML formatting option.

";

# Help and information.
if [[ $1 = '--help' ]]; then echo "$HELP"; exit ${EXIT_NORMAL}; fi;
if [[ $1 = '--version' ]]; then echo "$SCRIPT $VERSION ($DATE)"; exit ${EXIT_NORMAL}; fi;

###################################
# Arguments
###################################

output_file=${OUTPUT_FILE};

while getopts "hp:v" arg
do
    case ${arg} in
        p) output_file=$OPTARG;;
        v) echo "$VERSION"; exit;;
        h|*) echo "$SCRIPT <REQUIRED> [OPTIONS]"; exit;;
    esac
done

###################################
# Procedure
###################################

# Remove the existing file if it exists.
if [[ -f ${output_file} ]]; then rm $output_file; fi;

# This allows output commands to use >> without error.
touch ${output_file};

# Start the file.
cat >> ${output_file} << EOF
<html>
<head>
<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
<link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
</head>
<body>
<div class="container">
<h1>Projects</h1>
EOF

# Generate output for active projects.
echo "<h2>Active</h2>" >> ${output_file};
lsprojects --format=html --columns --html-linked --color >> ${output_file};

# Generate output for inactive projects.
echo "<h2>On Hold</h2>" >> ${output_file};
lsprojects --format=html --columns --html-linked --color --hold >> ${output_file};

# Generate output for archived projects.
echo "<h2>Archived</h2>" >> ${output_file};
lsprojects --format=html --columns --html-linked --color --archive >> ${output_file};

# Finish the file.
cat >> ${output_file} << EOF
</div>
</body>
</html>
EOF

# Clean up and exit.
#if [[ -f $TEMP_FILE ]]; then rm $TEMP_FILE; fi;
exit ${EXIT_NORMAL};
