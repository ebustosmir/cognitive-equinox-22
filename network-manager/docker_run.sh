#!/bin/bash
SCRIPT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT_FOLDER=${SCRIPT_FOLDER}/..

. "${PROJECT_ROOT_FOLDER}/tools/variables.sh"

docker rm -f ${HOST1_NAME} ${HOST2_NAME} ${HOST3_NAME} ${HOST4_NAME} ${HOST5_NAME}

. ${PROJECT_ROOT_FOLDER}/tools/start_networks.sh

docker run --name network-manager --network "${NETWORK_NAME}" --dns=172.20.0.2 --ip=172.20.0.3 -d -p 6001:5000 -e FLASK_APP=server -e SERVER_NAME=network-manager network-manager
