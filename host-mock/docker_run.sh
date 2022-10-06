docker run --name mock1 -d -p 5000:5000 -e FLASK_APP=server -e SERVER_NAME=serversito host-mock

docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mock1