# GIRS - Redis
A Redis Cluster deployment and management in a clusterized environment.
Ongoing project for GIRS (Gestão Integrada de Redes e Sistemas) course of MIECT, at DETI-UA (University of Aveiro).

The project goal is to manage and setup a high-availability service, such as Redis.

### Developers and collaborators:
- [Cristiano Vagos](http://github.com/cristianovagos)
- [Miguel Bras](http://github.com/miguelbras)
- [Marco Macedo](http://github.com/marcomacedo)

### Projects
Here we have two different approaches, one using Redis Cluster with 6 instances (3 Master / 3 Slave), and other approach
using a set of 3 Redis Sentinels, and 3 instances (1 Master, 2 Slave). 

Check them out here:

* [Redis Cluster](./redis-cluster/)
* [Redis Sentinel](./redis-sentinel/)
