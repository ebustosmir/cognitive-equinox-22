FROM ubuntu:bionic

COPY bin/docker-entrypoint.sh /home/docker-entrypoint.sh

RUN apt-get update \
  && apt-get install -y \
  bind9 \
  bind9utils \
  bind9-doc

# Enable IPv4
RUN sed -i 's/OPTIONS=.*/OPTIONS="-4 -u bind"/' /etc/default/bind9

# Copy configuration files
#COPY named.conf.options /etc/bind/
#COPY named.conf.local /etc/bind/
#COPY db.nagoya-foundation.com /etc/bind/zones/

ENTRYPOINT ["/home/docker-entrypoint.sh"]