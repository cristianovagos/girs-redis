#!/bin/bash

set -ex

echo "=> Creating HAProxy Configuration Folder"
mkdir -p /etc/haproxy


echo "=> Writing HAProxy Configuration File"
tee /etc/haproxy/haproxy.cfg <<EOF
defaults
  mode tcp
  timeout connect 3s
  timeout server 6s
  timeout client 6s
listen stats
  mode http
  bind :7020
  stats enable
  stats hide-version
  stats realm Haproxy\ Statistics
  stats uri /stats
frontend ft_redis
  mode tcp
  bind *:7010
  default_backend bk_redis
backend bk_redis
  balance roundrobin
  mode tcp
  option tcplog
  option tcp-check
  tcp-check send PING\r\n
  tcp-check expect string +PONG
  tcp-check send info\ replication\r\n
  tcp-check expect string role:master
  tcp-check send QUIT\r\n
  tcp-check expect string +OK
EOF

echo "=> Adding Redis Nodes to Health Check"
COUNT=1

for i in $(echo $REDIS_HOSTS | sed "s/,/ /g")
do
    echo "  server redis-$COUNT $i maxconn 1024 check inter 1s" >> /etc/haproxy/haproxy.cfg
    COUNT=$((COUNT + 1))
done

echo "=> Starting HAProxy"
exec "/docker-entrypoint.sh" "$@"