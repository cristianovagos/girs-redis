import time
import json
import sys

from rediscluster import RedisCluster

# FUNCAO PARA CALCULAR OS PARAMETROS DE PERFORMANCE
# results - array com os tempos de execução a cada 1000 pedidos
# data_len - numero de bits
def calculate(results, data_len):
#     IOPS
    sum = 0
    for line in results:
        sum += line
    iops = (len(results) * 1000)/sum
    # print("IOPS for data = " + str(data_len) + " bits = " + str(iops))

#     Latency
    latency = sum / len(results)
    # print("Latency for data = " + str(data_len) + " bits = " +str(latency))

#     Bandwidth
    bandwidth = (len(results) * 1000 * data_len) / sum
    # print("Bandwidth for data = " + str(data_len) + " bits = " + str(bandwidth))

    return ("NUM OF BITS = " + str(data_len),
            "IOPS = " + str(iops),
            "LATENCY = " + str(latency),
            "BANDWIDTH = " + str(bandwidth))


# FOR TESTING it should be 6 = 128 bits
starting_num = 6
# FOR TESTING it should be 23 = 8 Mega
ending_num = 23


# Initialize RedisCluster object
debug = False
host = "127.0.0.1" if debug else "192.168.215.21"
startup_nodes = [{"host": host, "port": "7000"},
                {"host": host, "port": "7001"},
                {"host": host, "port": "7002"},
                {"host": host, "port": "7003"},
                {"host": host, "port": "7004"},
                {"host": host, "port": "7005"}]
r = RedisCluster(startup_nodes=startup_nodes, max_connections=32, decode_responses=True)

# verificar tamanho de argumentos
if len(sys.argv) > 1:
    client_num = sys.argv[1]
else:
    client_num = "1"

results_set = results_get = []

# SET TEST
j=0
for i in range(starting_num, ending_num):
    timeout = time.time() + 10
    print("\nStarting SET test for " + str(pow(2, i+1)) + " bits")

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

print("SET test concluded, writing results on {} file\n".format("results-raw-set-client" + client_num + ".txt"))
f = open(str("results-raw-set-client{}.txt").format(client_num), "w")
f.write(json.dumps(results_set, indent=4))
f.close()

# GET TEST
j=0
for i in range(starting_num, ending_num):
    timeout = time.time() + 10
    print("\nStarting GET test for " + str(pow(2, i+1)) + " bits")

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

print("GET test concluded, writing results on {} file\n".format("results-raw-get-client" + client_num + ".txt"))
f = open(str("results-raw-get-client{}.txt").format(client_num), "w")
f.write(json.dumps(results_get, indent=4))
f.close()

# CALCULOS
data_len = pow(2, starting_num+1)
results = []
final_results_set = []
for line in results_set:
    current_data_len = line[1]

    if current_data_len != data_len:
        final_results_set.append(calculate(results, data_len))
        data_len = current_data_len
        results = []
        continue

    results.append(line[4] - line[3])

final_results_set.append(calculate(results, data_len))

print("Writing final results on {} file\n".format("results-set-client" + client_num + ".txt"))
f = open(str("results-set-client{}.txt").format(client_num), "w")
f.write(json.dumps(final_results_set, indent=4))
f.close()

data_len = pow(2, starting_num+1)
results = []
final_results_get = []
for line in results_get:
    current_data_len = line[1]

    if current_data_len != data_len:
        final_results_get.append(calculate(results, data_len))
        data_len = current_data_len
        results = []
        continue

    results.append(line[4] - line[3])

final_results_get.append(calculate(results, data_len))

print("Writing final results on {} file\n".format("results-get-client" + client_num + ".txt"))
f = open(str("results-get-client{}.txt").format(client_num), "w")
f.write(json.dumps(final_results_get, indent=4))
f.close()
