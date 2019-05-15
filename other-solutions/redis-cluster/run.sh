#!/bin/bash

# cria a rede overlay na swarm
docker network create -d overlay --attachable rediscluster_net

network=rediscluster_net

# configuração para cada cliente redis
REDIS_CONFIG='port 6379
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
appendonly no
maxmemory 2gb'

# comeca 6 replicas (3 masters, 3 slaves) do redis na rede que definimos, e com a config acima 
docker service create --name redis \
  --network $network \
  --replicas=6 \
  -e REDIS_CONFIG="$REDIS_CONFIG" \
  -e REDIS_CONFIG_FILE="/usr/local/etc/redis/redis.conf" \
  redis:5.0.4-alpine sh -c 'mkdir -p $(dirname $REDIS_CONFIG_FILE) && \
  echo "$REDIS_CONFIG" > $REDIS_CONFIG_FILE && \
  cat $REDIS_CONFIG_FILE && redis-server $REDIS_CONFIG_FILE'

# mostrar que esta tudo ok
sleep 2
docker service ps redis --no-trunc

# executa o comando para formar o redis cluster num dos containers que criamos acima
docker exec -it $(docker ps -f name=redis -q | head -n 1) redis-cli --cluster create \
 $(docker inspect $(docker node ps -f name=redis $(docker node ls -q) -q) -f '{{(index (index .NetworksAttachments) 0).Addresses}}' | sed 's|/.*||;s/[[]//' | awk '!a[$0]++' | awk '{printf $1 ":6379 "}') --cluster-replicas 1

cluster_node=$(docker inspect $(docker node ps -f name=redis $(docker node ls -q) -q) -f '{{(index (index .NetworksAttachments) 0).Addresses}}' | sed 's|/.*||;s/[[]//' | head -n 1)

# faz build a imagem do cliente 
docker build -t rediscluster-client ./client

# criar a imagem
docker create -it --name redisclient --network=$network -e CLUSTER_HOST=$cluster_node rediscluster-client

# arrancar a imagem
docker start redisclient

# ver a execucao do cliente
docker logs redisclient -f

