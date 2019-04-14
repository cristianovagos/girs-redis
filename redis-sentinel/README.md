# GIRS - Redis Sentinel Cluster
A Redis Cluster deployment and management in a clusterized environment.
Ongoing project for GIRS (Gestão Integrada de Redes e Sistemas) course of MIECT, at DETI-UA (University of Aveiro).

The project goal is to manage and setup a high-availability service, such as Redis.

### Developers and collaborators:
- [Cristiano Vagos](http://github.com/cristianovagos)
- [Miguel Bras](http://github.com/miguelbras)
- [Marco Macedo](http://github.com/marcomacedo)

### Info
This deployment will have 3 instances of Redis Sentinel, which will monitor the other 3 Redis instances that will 
be deployed. Initially, the cluster will have 1 Master and 2 Slaves, but the Sentinel instances will monitor the 
whole cluster and if the Master fails, they will elect a new Master. Redis will replicate the information kept on 
the Master instance to the Slaves. A important note: its only possible to write data to the Master instance, and 
because we don't know which of the instances is the Master, we will ask Sentinel which is the cluster Master, and then
we can write data onto it, but it's possible to get data from the Slaves, as they are readonly.

For now, this project has a Python client that will connect to the Redis cluster and perform multiple set/get operations
with various data sizes (from 128 bits up to 4Mbits) during a minute each. The results obtained will give us some
performance parameters to estimate the cluster usage.

The main difference from the redis-cluster package located on this repository is that this deployment needs no
connection onto the Docker Swarm network, as the outside IP address is announced to inside the Redis instances. We just
need to access the Redis Sentinel and ask for the address of the Master, and then access to it. The only downside
is that with this deployment we have no data sharding.


### How to run

Install Docker and docker-machine

Connect to a existing Docker Swarm
```sh
$ eval $(docker-machine env compute1)
```

Run the script
```sh
$ bash run.sh
```

This script will:
- create a overlay network on a connected Docker Swarm
- setup and run a Redis cluster, consisting on 3 Redis Sentinels, 1 Master and 2 Slaves

After the creation of the Redis Cluster deployment, run the Python client:
```sh
$ pip install -r requirements.txt          # install the packages needed
$ python client.py 1                       # run the Python client
```

The client will generate 4 files:
- _results-set-client1.txt_ (final results for set)
- _results-get-client1.txt_ (final results for get)
- _results-raw-set-client1.txt_ (raw results for set)
- _results-raw-get-client1.txt_ (raw results for get)

### Local development

It's possible to setup this Redis Cluster in a local development, using Virtualbox as a driver (_must be installed_).
To do it, you must create a Docker Swarm as follows:

For a master node do this:
```sh
$ docker-machine create -d virtualbox master
$ docker swarm init --advertise-addr eth1
```
A Docker Swarm token will be generated. Store it and use it to join workers.

For each worker do this:
```sh
$ docker-machine create -d virtualbox worker01
$ docker-machine ssh worker01
$ docker swarm join --token TOKEN
```