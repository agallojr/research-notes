from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

print("making circuit")
# Generate 3-qubit GHZ state
circ = QuantumCircuit(3)
circ.h(0)
circ.cx(0, 1)
circ.cx(1, 2)
circ.measure_all()

print("making simulator")
# Construct an ideal simulator
aersim = AerSimulator()
aersim.set_options()  # here we might set device='GPU'

# Transpile for simulator or specific hardware
print("transpiling")
circ = transpile(circ, aersim)

print("running")
result = aersim.run(circ).result()
counts = result.get_counts(circ)
print('Counts:', str(counts))


