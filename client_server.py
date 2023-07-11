from concrete import fhe
import random
import time

NUM_OF_RECORDS = 10000
print("Num of records ", NUM_OF_RECORDS)
#Server
server = fhe.Server.load("server.zip")

print("Server initialization DONE")
serialized_client_specs: str = server.client_specs.serialize()

#Client
client_specs = fhe.ClientSpecs.deserialize(serialized_client_specs)
client = fhe.Client(client_specs)

print("Client initialization DONE ")
client.keys.generate()
serialized_evaluation_keys: bytes = client.evaluation_keys.serialize()

print("Key generation DONE")
serialized_args_list = []
rnd_input_list = []
for idx in range(NUM_OF_RECORDS):
    rnd_input = random.randint(-256, 255)
    rnd_input_list.append(rnd_input)
    rnd_input = rnd_input + 256
    serialized_args: bytes = client.encrypt(rnd_input).serialize()
    serialized_args_list.append(serialized_args)

print("Encryption DONE")
#Server
deserialized_evaluation_keys = fhe.EvaluationKeys.deserialize(serialized_evaluation_keys)
deserialized_args_list = []
for idx in range(NUM_OF_RECORDS):
    deserialized_args  = server.client_specs.deserialize_public_args(serialized_args_list[idx])
    deserialized_args_list.append(deserialized_args)

print("Serialization DONE")
public_result_list = []
start_time = time.time()
for idx in range(NUM_OF_RECORDS):
    public_result = server.run(deserialized_args_list[idx], deserialized_evaluation_keys)
    public_result_list.append(public_result)
end_time = time.time()
exec_time_ms = (end_time - start_time) * 1000
print("Execution time: {:.2f} ms".format(exec_time_ms))


serialized_public_result_list = []
for idx in range(NUM_OF_RECORDS):
    serialized_public_result: bytes = public_result_list[idx].serialize()
    serialized_public_result_list.append(serialized_public_result)

#Client
for idx in range(NUM_OF_RECORDS):
    deserialized_public_result = client.specs.deserialize_public_result(serialized_public_result_list[idx])
    result = client.decrypt(deserialized_public_result)
    print(rnd_input_list[idx], ' has sign ', result)