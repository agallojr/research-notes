from qiskit.circuit.library import EfficientSU2
import numpy as np
from qiskit.circuit.library import UnitaryOverlap
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import matplotlib.pyplot as plt
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import EstimatorV2 as Estimator, EstimatorOptions
import statistics
from qc_grader.challenges.qgss_2024 import *

num_qubits = 50 # 50 
reps = 2
default_shots = 10_000


abstract_circuit = EfficientSU2(num_qubits, reps=reps, entanglement="pairwise")

num_parameters = abstract_circuit.num_parameters
param_values = np.random.uniform(-np.pi, np.pi, size=num_parameters)
abstract_circuit.assign_parameters(param_values, inplace=True)

# make a barrier then make a mirror of the circuit
abstract_circuit.barrier()
abstract_circuit = UnitaryOverlap(abstract_circuit, abstract_circuit)

# make observables
paulis = ["".join("Z" if i == q else "I" \
    for i in range(num_qubits)) for q in range(num_qubits)]
abstract_observables = [SparsePauliOp(pauli) for pauli in paulis]

# assign a backend 
service = QiskitRuntimeService()
backend = service.least_busy(min_num_qubits=127)
#backend = AerSimulator()

# transpilation to a runnable circuit & observables on this backend
pm = generate_preset_pass_manager(backend=backend, optimization_level=3)
target_circuit = pm.run(abstract_circuit)
layout = target_circuit.layout
target_observables = [abs_obs.apply_layout(layout=layout) \
    for abs_obs in abstract_observables]


#******************************************************************
# define the run, run it, analyze the results

def run1():
    # Define Estimator
    estimator = Estimator(mode=backend)
    options = estimator.options

    # Turn off all error mitigation and suppression
    options.resilience_level = 0
    options.optimization_level = 0
    options.default_shots = default_shots

    # Define the primitive unified bloc (PUB) for Estimator jobs
    pub = (target_circuit, target_observables)

    result = estimator.run([pub]).result()[0]
    print("run 1 = " + str(statistics.mean(result.data.evs)))


def run2():
    # Define Estimator
    estimator = Estimator(mode=backend)
    options = estimator.options

    # Turn off all error mitigation and suppression
    options.resilience_level = 0
    options.optimization_level = 0
    options.default_shots = default_shots

    # Turn on for dynamical decoupling
    options.dynamical_decoupling.enable = True
    options.dynamical_decoupling.sequence_type = "XX"

    # Define the primitive unified bloc (PUB) for Estimator jobs
    pub = (target_circuit, target_observables)

    result = estimator.run([pub]).result()[0]
    print("run 2 = " + str(statistics.mean(result.data.evs)))


def run3():
    # Define Estimator
    estimator = Estimator(mode=backend)
    options = estimator.options

    # Turn off all error mitigation and suppression
    options.resilience_level = 0
    options.optimization_level = 0
    options.default_shots = default_shots

    # Turn on for TREX measurement mitigation
    options.resilience_level = 1
    options.resilience.measure_mitigation = True
    # there are many other options & techniques for measurement mitigation
    # run #4a & b of this exercise uses the ZNE technique.  run #5 uses Gate 
    # Twirling.  run #6 uses all of the above.
    # and we expect to converge on a mean of 1 as the techniques improve 
    # the resilience of the results.

    # Define the primitive unified bloc (PUB) for Estimator jobs
    pub = (target_circuit, target_observables)

    result = estimator.run([pub]).result()[0]
    print("run 3 = " + str(statistics.mean(result.data.evs)))


#******************************************************************
# main program

run3()

