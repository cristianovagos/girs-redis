import time
import json
import sys
import os
from redis.sentinel import Sentinel

# FUNCAO PARA CALCULAR OS PARAMETROS DE PERFORMANCE
# results - array com os tempos de execução a cada 1000 pedidos
# data_len - numero de bits
def calculate(results, data_len, num_errors):
    if len(results) > 0:
        sum = 0
        for line in results:
            sum += line

        iops = (len(results) * 1000) / sum
        latency = sum / len(results)
        bandwidth = (len(results) * 1000 * data_len) / sum
        errors = (num_errors / (len(results) * 1000)) * 100
    else:
        iops = latency = bandwidth = "N/A"
        errors = 100

    return ("NUM OF BITS = " + str(data_len),
            "ERROR PERCENTAGE = " + str(errors) + "%",
            "IOPS = " + str(iops),
            "LATENCY = " + str(latency),
            "BANDWIDTH = " + str(bandwidth))

# FOR TESTING it should be 6 = 128 bits
starting_num = 6
# FOR TESTING it should be 23 = 8 Mega
ending_num = 23

debug = True
host = "192.168.99.100" if debug else ""
sentinel = Sentinel([(host, 7010)], socket_timeout=0.1)
r = sentinel.master_for('mymaster', socket_timeout=0.1)

# verificar tamanho de argumentos
if len(sys.argv) > 1:
    client_num = sys.argv[1]
else:
    client_num = "1"

results_set = []
results_get = []
num_of_requests = dict()

# SET TEST
for i in range(starting_num, ending_num):
    print("\nStarting SET test for " + str(pow(2, i+1)) + " bits")

    # generate string of 2^n zeros, starting with 128
    data = "0" * pow(2, i + 1)
    data_len = len(data)
    j = 0
    timeout = time.time() + 60
    while time.time() < timeout:
        time_aux = time.time()
        errors = 0
        for count in range(1000):
            try:
                result = r.set("test_key-{}".format(j), data)
                if result == "False":
                    errors += 1
            except Exception as e:
                errors += 1
            j += 1

        m = (j, data_len, errors, time_aux, time.time())
        num_of_requests[data_len] = j
        results_set.append(m)

print("SET test concluded, writing results on {} file\n".format("results-raw-set-client" + client_num + ".txt"))
f = open(str("results-raw-set-client{}.txt").format(client_num), "w")
f.write(json.dumps(results_set, indent=4))
f.close()

# GET TEST
print("num_of_requests = " + str(num_of_requests))
for i in range(starting_num, ending_num):
    print("\nStarting GET test for " + str(pow(2, i+1)) + " bits")

    timeout = time.time() + 60
    data_len = int(pow(2, i+1))

    j = 0
    breaking = False
    count_aux = 1
    aux = num_of_requests[data_len]
    while time.time() < timeout:
        time_aux = time.time()
        errors = 0
        for count in range(1000):
            if count_aux*1000 <= aux:
                try:
                    result = r.get("test_key-{}".format(j))
                    if result is None:
                        errors += 1
                except Exception as e:
                    errors += 1
                j += 1
            else:
                print("breaking... bits = " + str(pow(2,i+1)) + ", count = " + str(count) + ", count_aux = " + str(count_aux))
                breaking = True
                break

        if breaking:
            break

        m = (j, data_len, errors, time_aux, time.time())

        results_get.append(m)
        count_aux += 1
        print("bits = " + str(pow(2,i+1)) + ", count_aux = " + str(count_aux))

print("GET test concluded, writing results on {} file\n".format("results-raw-get-client" + client_num + ".txt"))
f = open(str("results-raw-get-client{}.txt").format(client_num), "w")
f.write(json.dumps(results_get, indent=4))
f.close()

# CALCULOS
data_len = pow(2, starting_num+1)
results = []
errors = 0
final_results_set = []
for line in results_set:
    current_data_len = line[1]

    if current_data_len != data_len:
        final_results_set.append(calculate(results, data_len, errors))
        data_len = current_data_len
        results = []
        errors = 0
        continue

    results.append(line[4] - line[3])
    errors += int(line[2])

final_results_set.append(calculate(results, data_len, errors))

print("Writing final results on {} file\n".format("results-set-client" + client_num + ".txt"))
f = open(str("results-set-client{}.txt").format(client_num), "w")
f.write(json.dumps(final_results_set, indent=4))
f.close()

data_len = pow(2, starting_num+1)
results = []
errors = 0
final_results_get = []
for line in results_get:
    current_data_len = line[1]

    if current_data_len != data_len:
        final_results_get.append(calculate(results, data_len, errors))
        data_len = current_data_len
        results = []
        errors = 0
        continue

    results.append(line[4] - line[3])
    errors += int(line[2])

final_results_get.append(calculate(results, data_len, errors))

print("Writing final results on {} file\n".format("results-get-client" + client_num + ".txt"))
f = open(str("results-get-client{}.txt").format(client_num), "w")
f.write(json.dumps(final_results_get, indent=4))
f.close()
