import pennylane as qml
from pennylane import numpy as np   # note this is pennylane's numpy wrapper 
from scipy.optimize import minimize


# optimize a NumPy-interfacing QNode (below) such that the weights x lead to a final 
# expectation value of 0.5

dev = qml.device('default.qubit', wires=2)

@qml.qnode(dev)
def circuit(x):
    qml.RX(x[0], wires=0)
    qml.RZ(x[1], wires=1)
    qml.CNOT(wires=[0, 1])
    qml.RX(x[2], wires=0)
    return qml.expval(qml.PauliZ(0))

def cost(x):
    return np.abs(circuit(x) - 0.5)**2

params = np.array([0.011, 0.012, 0.05], requires_grad=True)

print(minimize(cost, params, method='BFGS', jac=qml.grad(cost, argnum=0)))
