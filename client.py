import time
import json

from rediscluster import RedisCluster

debug = True
host = "127.0.0.1" if debug else "192.168.215.21"
startup_nodes = [{"host": host, "port": "7000"},
                {"host": host, "port": "7001"},
                {"host": host, "port": "7002"},
                {"host": host, "port": "7003"},
                {"host": host, "port": "7004"},
                {"host": host, "port": "7005"}]
r = RedisCluster(startup_nodes=startup_nodes, max_connections=32, decode_responses=True)

results_set = results_get = []

# loop until 1 million
j=0
for i in range(20, 23):
    timeout = time.time() + 10
    print("\nStarting SET test for i=" + str(i))

    # generate string of 2^n zeros, starting with 128
    data = "0" * pow(2, i + 1)
    data_len = len(data)
    while time.time() < timeout:
        time_aux = time.time()
        errors = 0
        for count in range(1000):
            result = r.set("test_key-{}".format(j), data)
            if result == "False":
                errors += 1
            j += 1

        m = (j, data_len, errors, time_aux, time.time())

        results_set.append(m)

print("SET test concluded, writing results on {} file\n".format("results-set.txt"))
f = open("results-set.txt", "w")
f.write(json.dumps(results_set, indent=4))
f.close()

# GET TEST

j=0
for i in range(20, 23):
    timeout = time.time() + 10
    print("\nStarting GET test for i=" + str(i))

    while time.time() < timeout:
        time_aux = time.time()
        errors = 0
        for count in range(1000):
            result = r.get("test_key-{}".format(j))
            if result is None:
                errors += 1
            j += 1

        m = (j, data_len, errors, time_aux, time.time())

        results_get.append(m)


print("GET test concluded, writing results on {} file\n".format("results-get.txt"))
f = open("results-get.txt", "w")
f.write(json.dumps(results_get, indent=4))
f.close()

# CALCULOS

#Calcular tempo resultante GET
result_time_get = 0
for i in range(len(results_get)):
        aux = results_get[i][3] - results_get[i][4]
        result_time_get += aux
print(result_time_get)

#Calcular tempo resultante SET
result_time_set = 0
for i in range(len(results_set)):
        aux = results_set[i][3] - results_set[i][4]
        result_time_set += aux
print(result_time_set)

#IOPS


