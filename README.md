# GIRS - Redis
A Redis Cluster deployment and management in a clusterized environment.
Ongoing project for GIRS (Gestão Integrada de Redes e Sistemas) course of MIECT, at DETI-UA (University of Aveiro).

The project goal is to manage and setup a high-availability service, such as Redis.

### Developers and collaborators:
- [Cristiano Vagos](http://github.com/cristianovagos)
- [Miguel Bras](http://github.com/miguelbras)
- [Marco Macedo](http://github.com/marcomacedo)

### Info
Initially we built three different approaches, using a simple Redis Cluster (3 Master / 3 Slave), and other using a set of 3 Redis Sentinels, with 3 instances each (1 Master, 2 Slave).

During the development we figured out that using a Redis Cluster infrastructure is the way to go, providing features such as data sharding and automatic failover, so we will stick with this solution, providing a high-availability service using multiple tools (load balancing, monitoring, etc). We will continue to update the _main_ folder, which will have the work we will deploy and test to the course requirements.

Main development:
* [**Redis Cluster**](./main/) (_**active development**_)

Other solutions:
* [~~Redis Cluster~~](./other-solutions/redis-cluster/) (_Deprecated. Working for demo issues_)
* [~~Redis Sentinel~~](./other-solutions/redis-sentinel/) (_Deprecated. Working for demo issues_)

Please read each README for more details and information.