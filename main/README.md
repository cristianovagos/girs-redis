# GIRS - Redis Cluster
A Redis Cluster deployment and management in a clusterized environment.
Ongoing project for GIRS (Gestão Integrada de Redes e Sistemas) course of MIECT, at DETI-UA (University of Aveiro).

The project goal is to manage and setup a high-availability service, such as Redis.

### Developers and collaborators:
- [Cristiano Vagos](http://github.com/cristianovagos)
- [Miguel Bras](http://github.com/miguelbras)
- [Marco Macedo](http://github.com/marcomacedo)

### Info
Initially, this deployment will launch 6 instances of Redis, which will later be built as a Redis Cluster, consisting on a 
3 Master, 3 Slave architecture. The _redis-cli_ client will suggest one cluster architecture, which will be the one
accepted and formed.

For load balancing, we will have _at least_ two machines, each having keepalived and HAProxy installed for high availability,
keepalived providing automatic failover using VRRP, and HAProxy doing load balancing among the Redis Cluster Masters with TCP, as well as
both having periodic healthchecks to monitor current status.
A stats page is also included for node monitoring and displaying current status of the Masters. This way, we will have a single floating
IP address that will connect to a single Master instance of our Redis Cluster.

For now, this project has a Python client that will connect to the Redis cluster and perform multiple set/get operations
with various data sizes (from 128 bits up to 4Mbits) during a minute each. The results obtained will give us some
performance parameters to estimate the cluster usage.

### TODO
* Monitoring
* Automation (combined with Monitoring, from infrastructure Alarms)

#### Why is this deployment preffered

Redis Cluster is a tool that provides replication and automatic failover, such as Redis Sentinel, but with data 
sharding added. We decided to stick with this architecture because a Redis Sentinel architecture will only accept 
1 Master, and only permits writes to it, whereas the Slaves are readonly. Having a Redis Cluster architecture will 
provide the same benefits of Redis Sentinel, but with the powerful capabilities of this tool, while having multiple 
Master and Slave instances working.

HAProxy and keepalived were added to the architecture to perform load balancing among the cluster.
keepalived does layer 3/4 load balancing, while having HAProxy choosing the Redis Cluster Masters in a roundrobin fashion,
so for each client connection HAProxy will select one of the Masters for client connection. In that way we offer a single
point of access for client connection to the Redis Cluster. HAProxy also provides a stats page that may be useful for
real-time monitoring of the Redis Cluster nodes status.

### How to run

Install Docker, docker-machine and Vagrant (virtualbox may also be needed)

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
- build, create and run two custom instances of HAProxy with keepalived for load balancing (using Vagrant)

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


### Useful info
- Redis Cluster single point of access: _<SWARM_MASTER_IP>:7010_
- HAProxy stats page: _<SWARM_MASTER_IP>:7020/stats_

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