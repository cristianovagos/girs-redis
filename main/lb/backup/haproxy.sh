#!/bin/bash

echo "--------------------"
echo "Installing HAProxy"
echo "--------------------"
apt-get install -y haproxy systemd

echo "Configure HAProxy Logging (rsyslog)"
sed -i 's/\#\$ModLoad imudp/\$ModLoad imudp/' /etc/rsyslog.conf
sed -i 's/\#\$UDPServerRun 514/\$UDPServerRun 514/' /etc/rsyslog.conf
echo "local2.* /var/log/haproxy.log" > /etc/rsyslog.d/haproxy.conf
systemctl restart rsyslog

cat > /etc/haproxy/haproxy.cfg <<EOF
global
	log         127.0.0.1 local2
	chroot      /var/lib/haproxy
	pidfile     /var/run/haproxy.pid
	maxconn     4000
	user        haproxy
	group       haproxy
	daemon
	# turn on stats unix socket
	stats socket /var/lib/haproxy/stats level admin
defaults
	mode                    http
	log                     global
	option                  httplog
	option                  dontlognull
	option http-server-close
	option forwardfor       except 127.0.0.0/8
	option                  redispatch
	retries                 3
	timeout http-request    10s
	timeout queue           1m
	timeout connect         10s
	timeout client          1m
	timeout server          1m
	timeout http-keep-alive 10s
	timeout check           10s
	maxconn                 3000
frontend ft_redis
    mode tcp
    bind *:80
    default_backend bk_redis
# Configure statistics page
listen stats
	mode http
    bind :9000
	stats enable
	stats hide-version
	stats realm HAproxy\ Statistics
	stats uri /stats
	stats auth admin:admin
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
    server redis-1 192.168.215.21:7001 maxconn 1024 check inter 1s
    server redis-2 192.168.215.21:7002 maxconn 1024 check inter 1s
    server redis-3 192.168.215.21:7003 maxconn 1024 check inter 1s
    server redis-4 192.168.215.21:7004 maxconn 1024 check inter 1s
    server redis-5 192.168.215.21:7005 maxconn 1024 check inter 1s
    server redis-6 192.168.215.21:7006 maxconn 1024 check inter 1s
EOF

systemctl enable haproxy
systemctl start haproxy


echo "Installing keepalived"
apt-get install -y keepalived
systemctl enable keepalived

sleep 10

systemctl restart haproxy