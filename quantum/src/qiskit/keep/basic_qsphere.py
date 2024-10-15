from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_state_qsphere
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# make the circuit 
circ = QuantumCircuit(3)
circ.h(0)
circ.cx(0, 1)
circ.cx(1, 2)

# make a drawing of the circuit 
circ.draw(output="mpl")

# make a qsphere plot of the state
state = Statevector(circ)
plot_state_qsphere(state)

# show the plots in separate windows
plt.show()

# now add the measurements 
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


