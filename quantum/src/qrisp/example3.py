from qiskit_aer import AerSimulator
from qrisp.interface import VirtualQiskitBackend

backend = AerSimulator()
vrtl_qasm_sim = VirtualQiskitBackend(backend)

from qrisp import QuantumArray, QuantumFloat, inplace_matrix_app
import numpy as np

import random

def generate_random_inv_matrix(n, bit):
    found = False

    while found == False:
        matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                matrix[i, j] = random.randint(0, 2 ** bit - 1)

        det = np.round(np.linalg.det(matrix) % 2 ** bit)

        found = bool(det%2)

    return matrix

bit = 5
n = 3

qtype = QuantumFloat(bit)
vector = QuantumArray(qtype = qtype, shape = n)

x_values = np.array([0, 2, 1])
vector[:] = x_values

matrix = generate_random_inv_matrix(n, bit)

inplace_matrix_app(vector, matrix)
print("***")
print(vector)

from qrisp import z, ry, QuantumBool, amplitude_amplification

def state_function(qb):
    ry(np.pi/8,qb)

def oracle_function(qb):   
    z(qb)

qb = QuantumBool()
amplitude_amplification([qb], state_function, oracle_function)
#res = qv.get_measurement(backend = backend)


