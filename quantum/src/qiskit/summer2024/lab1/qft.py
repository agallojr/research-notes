
from qiskit.circuit.library import QFT
import matplotlib.pyplot as plt


# get an abstract quantum circuit from Qiskit's library of circuits 
num_qubits = 10
qc = QFT(num_qubits, do_swaps=False)
qc.draw(output="mpl")
plt.show()

