FROM ubuntu:bionic

RUN apt-get update \
  && apt-get install -y \
  bind9 \
  bind9utils \
  bind9-doc

# Enable IPv4
RUN sed -i 's/OPTIONS=.*/OPTIONS="-4 -u bind"/' /etc/default/bind9

# Copy configuration files
COPY bin/docker-entrypoint.sh /home/docker-entrypoint.sh
RUN chmod +x /home/docker-entrypoint.sh

COPY etc/named.conf.options /etc/bind/
COPY etc/named.conf.local /etc/bind/
COPY etc/named.conf.logging /etc/bind/
COPY etc/named.conf /etc/bind/

RUN mkdir -p /var/log/bind
RUN chown bind:bind /var/log/bind




ENTRYPOINT ["/home/docker-entrypoint.sh"]