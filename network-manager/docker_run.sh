#!/bin/bash
SCRIPT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT_FOLDER=${SCRIPT_FOLDER}/..

. "${PROJECT_ROOT_FOLDER}/tools/variables.sh"

docker rm -f network-manager

docker run -it --name network-manager --network "${NETWORK_NAME}" --dns=172.20.0.2 --ip=172.20.0.3 -d -p 80:5000 -e FLASK_APP=server -e SERVER_NAME=network-manager -v "${PROJECT_ROOT_FOLDER}/volume/db.cognitive-equinox.com":/home/db.cognitive-equinox.com network-manager
