#!/bin/bash
SCRIPT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT_FOLDER=${SCRIPT_FOLDER}/..

. "${PROJECT_ROOT_FOLDER}/tools/variables.sh"

docker rm -f ${HOST1_NAME} ${HOST2_NAME} ${HOST3_NAME} ${HOST4_NAME} ${HOST5_NAME}

. ${PROJECT_ROOT_FOLDER}/tools/start_networks.sh

docker run --name ${HOST1_NAME} --network "${NETWORK_NAME}" --dns=172.20.0.2 --ip=172.20.0.3 -d -p 6001:5000 -e FLASK_APP=server -e SERVER_NAME=${HOST1_NAME} host-mock
docker run --name ${HOST2_NAME} --network "${NETWORK_NAME}" --dns=172.20.0.2 --ip=172.20.0.4 -d -p 6002:5000 -e FLASK_APP=server -e SERVER_NAME=${HOST2_NAME} host-mock
docker run --name ${HOST3_NAME} --network "${NETWORK_NAME}" --dns=172.20.0.2 --ip=172.20.0.5 -d -p 6003:5000 -e FLASK_APP=server -e SERVER_NAME=${HOST3_NAME} host-mock
docker run --name ${HOST4_NAME} --network "${NETWORK_NAME}" --dns=172.20.0.2 --ip=172.20.0.6 -d -p 6004:5000 -e FLASK_APP=server -e SERVER_NAME=${HOST4_NAME} host-mock
docker run --name ${HOST5_NAME} --network "${NETWORK_NAME}" --dns=172.20.0.2 --ip=172.20.0.7 -d -p 6005:5000 -e FLASK_APP=server -e SERVER_NAME=${HOST5_NAME} host-mock
