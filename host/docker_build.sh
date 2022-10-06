#!/bin/bash

SCRIPT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT_FOLDER=${SCRIPT_FOLDER}/..

docker build -t host ${PROJECT_ROOT_FOLDER}/host