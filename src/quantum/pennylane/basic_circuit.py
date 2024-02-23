import pennylane as qml
import numpy as np

def my_quantum_function(x, y):
    qml.RZ(x, wires=0)
    qml.CNOT(wires=[0,1])
    qml.RY(y, wires=1)
    return qml.expval(qml.PauliZ(1))

dev = qml.device('default.qubit', wires=2, shots=1000)
circuit = qml.QNode(my_quantum_function, dev)

print(circuit(np.pi/4, 0.7))
print(qml.draw(circuit)(np.pi/4, 0.7))
