FROM python:3.9.14-slim

LABEL name="aura-cognitive/hot-mock" \
      maintainer="Telefonica <telefonica@telefonica.com>" \
      vendor="Telefonica" \
      license="Telefonica"

ARG FLASK_APP
ARG SERVER_NAME

EXPOSE 5000

COPY bin/docker-entrypoint.sh /home/docker-entrypoint.sh
RUN chmod +x /home/docker-entrypoint.sh

COPY requirements.txt /home/requirements.txt
COPY run-server.sh /home/run-server.sh
COPY server.py /home/server.py


RUN pip install -r /home/requirements.txt

WORKDIR /home


ENTRYPOINT ["/home/docker-entrypoint.sh"]