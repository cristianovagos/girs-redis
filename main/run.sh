#!/bin/bash

printf "GIRS 2019 - Redis Cluster\nCristiano Vagos, Miguel Bras, Marco Macedo\n\n"
printf "Creating overlay network...\n"

# IP do swarm manager
swarm_master=192.168.99.100

# IP virtual (floating IP)
virtual_ip_addr=10.0.0.123

# cria a rede overlay na swarm
docker network create -d overlay --attachable rediscluster_net
network=rediscluster_net

for ind in `seq 1 6`; do \
 printf "\nCreating redis-$ind instance...\n"

 docker service create \
    --name "redis-$ind" \
    --network $network \
    -e REDIS_CONFIG="
    port 700$ind
    cluster-enabled yes
    cluster-config-file nodes.conf
    cluster-node-timeout 5000
    cluster-announce-ip $swarm_master
    appendonly no
    maxmemory 1gb
    maxmemory-policy allkeys-lru
    " \
    -p "700$ind:700$ind" \
    -p "1700$ind:1700$ind" \
    -e REDIS_CONFIG_FILE="/usr/local/etc/redis/redis.conf" \
    redis:alpine sh -c 'mkdir -p $(dirname $REDIS_CONFIG_FILE) && \
    echo "$REDIS_CONFIG" > $REDIS_CONFIG_FILE && \
    cat $REDIS_CONFIG_FILE && redis-server $REDIS_CONFIG_FILE'
done

sleep 2

printf "\nCreating a redis cluster based on the instances created...\nWrite 'yes' to confirm the cluster structure\n"

first_redis=$(docker ps -f name=redis -q | head -n 1)
docker exec -it $first_redis redis-cli --cluster create \
  $(for ind in `seq 1 6`; do \
  echo -n "$swarm_master:700$ind "
  done) --cluster-replicas 1

printf "\nCreating 2 custom HAProxy + keepalived instances for load balancing onto the Redis Cluster...\n"

cd ./lb/
vagrant up

printf "\nAll done and up. Enjoy Redis Cluster!\n"