from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_state_qsphere
import matplotlib.pyplot as plt

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
