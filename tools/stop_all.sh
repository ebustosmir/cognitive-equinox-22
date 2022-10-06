
SCRIPT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT_FOLDER=${SCRIPT_FOLDER}/..
. "${PROJECT_ROOT_FOLDER}/tools/variables.sh"

docker stop ${HOST1_NAME}
docker stop ${HOST2_NAME}
docker stop ${HOST3_NAME}
docker stop ${HOST4_NAME}
docker stop ${HOST5_NAME}
docker stop network-manager
docker stop dns-server
