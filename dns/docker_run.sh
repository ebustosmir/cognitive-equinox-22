SCRIPT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT_FOLDER=${SCRIPT_FOLDER}/..
. "${PROJECT_ROOT_FOLDER}/tools/variables.sh"

docker rm -f dns-server || true
. ${PROJECT_ROOT_FOLDER}/tools/start_networks.sh
docker run -t -d --name=dns-server --net=${NETWORK_NAME} --ip=172.20.0.2 --entrypoint=/bin/bash -v "${PROJECT_ROOT_FOLDER}/volume/db.cognitive-equinox":/etc/bind/db.cognitive-equinox bind9
