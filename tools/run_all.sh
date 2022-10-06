#!/bin/bash

SCRIPT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT_FOLDER=${SCRIPT_FOLDER}/..

echo "BUILD DNS"
. ${PROJECT_ROOT_FOLDER}/dns/docker_build.sh

echo "BUILD host"
. ${PROJECT_ROOT_FOLDER}/host/docker_build.sh

echo "RUN NETWORK"
. ${PROJECT_ROOT_FOLDER}/tools/start_network.sh

echo "RUN DNS"
. ${PROJECT_ROOT_FOLDER}/dns/docker_run.sh

echo "RUN host"
. ${PROJECT_ROOT_FOLDER}/host/docker_run.sh