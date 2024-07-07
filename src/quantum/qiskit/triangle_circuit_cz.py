from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix
from qiskit.visualization import plot_state_qsphere, plot_state_city
import matplotlib.pyplot as plt

# make the circuit 
circ = QuantumCircuit(3)
circ.h(0)
circ.h(1)
circ.h(2)
circ.cz(0, 1)
circ.cz(1, 2)
circ.cz(0, 2)

# make a drawing of the circuit 
circ.draw(output="mpl")

# make a qsphere plot of the state
state = Statevector(circ)
plot_state_qsphere(state, show_state_phases=True)
den = DensityMatrix(circ)
plot_state_city(den)

# show the plots in separate windows
plt.show()
