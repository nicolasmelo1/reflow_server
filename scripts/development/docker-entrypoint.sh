#!/bin/bash
# With this we can use host.docker.internal to access a the localhost
# of the machine instead of the container, similarly to Docker for Mac
# and Docker for Windows. This way we can connect docker containers with each other

HOST_DOMAIN="host.docker.internal"
ping -q -c1 $HOST_DOMAIN > /dev/null 2>&1
if [ $? -ne 0 ]; then
  HOST_IP=$(ip route | awk 'NR==1 {print $3}')
  echo -e "$HOST_IP\t$HOST_DOMAIN" >> /etc/hosts
fi