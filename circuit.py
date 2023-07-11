from concrete import fhe
import numpy as np

def generate_sign_table(max):
    sign = []
    for idx in range(-max, 0):
        sign.append(-1)
    sign.append(0)
    for idx in range(1, max + 1):
        sign.append(1)

    table = fhe.LookupTable(sign)
    return table

table = generate_sign_table(256)
@fhe.compiler({"x": "encrypted"})
def f(x):
    return table[x]

inputset = range(512)
circuit = f.compile(inputset)
circuit.server.save("server.zip")
