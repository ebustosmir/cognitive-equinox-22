FROM python:3.9.14-slim

LABEL name="cognitive-equinox/hot-mock"

ARG FLASK_APP
ARG SERVER_NAME
RUN apt-get update && apt-get upgrade && apt-get install -y iputils-ping
COPY bin/docker-entrypoint.sh /home/docker-entrypoint.sh
RUN chmod +x /home/docker-entrypoint.sh

COPY requirements.txt /home/requirements.txt
COPY server.py /home/server.py


RUN pip install -r /home/requirements.txt

WORKDIR /home


ENTRYPOINT ["/home/docker-entrypoint.sh"]