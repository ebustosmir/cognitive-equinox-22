#!/bin/bash
# $1: name
# $2: port
docker run --name $1 -d -p $2:5000 -e FLASK_APP=server -e SERVER_NAME=$1 host-mock
