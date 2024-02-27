import pennylane as qml
import numpy as np

# device as a variable to permit same code on different devices 
dev = qml.device('default.qubit', wires=2, shots=1000)

@qml.qnode(dev) 
def circuit1(x, y):
    qml.RZ(x, wires=0)
    qml.CNOT(wires=[0,1])
    qml.RY(y, wires=1)
    return qml.expval(qml.PauliZ(1))

print(circuit1(np.pi/4, 0.7))
print(qml.draw(circuit1)(np.pi/4, 0.7))



