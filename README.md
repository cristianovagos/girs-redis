# GIRS - Redis Cluster
A Redis Cluster deployment and management in a clusterized environment.
Ongoing project for GIRS (Gestão Integrada de Redes e Sistemas) course of MIECT, at DETI-UA (University of Aveiro).

The project goal is to manage and setup a high-availability service, such as Redis.

### Developers and collaborators:
- [Cristiano Vagos](http://github.com/cristianovagos)
- [Miguel Bras](http://github.com/miguelbras)
- [Marco Macedo](http://github.com/marcomacedo)

### Instructions
For now, this project has a Python client that will connect to the Redis cluster and perform multiple set/get operations
with various data sizes (from 128 bits up to 4Mbits) during a minute each. The results obtained will give us some
performance parameters to estimate the cluster usage.

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
- setup and run 6 replicas of Redis
- create a Redis cluster using the redis-cli tool (when prompted, write 'yes' to accept the cluster structure this tool suggests)
- build, create and run a container with our Python client

After the client has concluded, the Python container will be stopped.
To transfer the files generated with the results do the following:
```sh
$ docker cp redisclient:/app .
```
It will copy the folder 'app' to the current location.

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