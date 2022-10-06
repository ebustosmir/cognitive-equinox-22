#!/bin/bash
SCRIPT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT_FOLDER=${SCRIPT_FOLDER}/..
. "${PROJECT_ROOT_FOLDER}/tools/variables.sh"

docker network create --subnet=172.20.0.0/16 ${NETWORK_NAME} || True