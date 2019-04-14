#!/bin/bash

# cria a rede overlay na swarm
docker network create -d overlay --attachable rediscluster_net

network=rediscluster_net
SWARM_MASTER=192.168.99.100

# Configuração do Master
docker service create  \
--name redis-master \
--network=rediscluster_net \
--publish 7000:6379 \
--replicas 1 \
redis:alpine redis-server  \
--port 6379;

# Configuração do Slave1
docker service create  \
--name redis-slave-1 \
--network=rediscluster_net \
--publish 7001:6380 \
--replicas 1 \
redis:alpine redis-server \
 --slaveof redis-master 6379  \
 --port 6380 \
 --slave-announce-ip $SWARM_MASTER

# Configuração do Slave2
docker service create  \
--name redis-slave-2 \
--network=rediscluster_net \
--publish 7002:6381 \
--replicas 1 \
redis:alpine redis-server  \
--slaveof redis-master 6379  \
--port 6381 \
--slave-announce-ip $SWARM_MASTER

# Configuração dos Redis Sentinels
docker service create \
--replicas 3 \
 --name redis-sentinel \
 --publish 7010:26379 \
redis:alpine \
sh -c "\
echo -e 'port 26379\n\
dir /tmp \n\
sentinel monitor mymaster $SWARM_MASTER 7000 2\n\
sentinel down-after-milliseconds mymaster 5000\n\
sentinel parallel-syncs mymaster 1\n\
sentinel failover-timeout mymaster 10000\n\
sentinel announce-ip $SWARM_MASTER\n\
' >  sentinel.conf; \
redis-server \
sentinel.conf \
--sentinel \
";
