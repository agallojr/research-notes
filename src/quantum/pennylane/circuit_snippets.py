import pennylane as qml
from pennylane import numpy as np

# pennylane lightning (fast C++ impl) simulator
dev1 = qml.device('lightning.qubit', wires=1, shots=10000)
#dev2 = qml.device('lightning.qubit', wires=2, shots=1000)
#dev3 = qml.device('lightning.qubit', wires=3, shots=1000)


dev = dev1

# ---------------------------------------------------------------------------

@qml.qnode(dev)
def getInitialState(): 
    return qml.state()

@qml.qnode(dev)
def pz():
    qml.PauliZ(0)
    return qml.state()

@qml.qnode(dev)
def pz_exp():
    return qml.expval(qml.PauliZ(0))

@qml.qnode(dev)
def pz_sample():
    return qml.sample(qml.PauliZ(0))

@qml.qnode(dev)
def flip():
    qml.PauliX(0)
    return qml.state()

@qml.qnode(dev)
def flip_pz():
    qml.PauliX(0)
    qml.PauliZ(0)
    return qml.state()

@qml.qnode(dev)
def flip_pz_exp():
    qml.PauliX(0)
    return qml.expval(qml.PauliZ(0))

@qml.qnode(dev)
def flip_pz_sample():
    qml.PauliX(0)
    return qml.sample(qml.PauliZ(0))


@qml.qnode(dev)
def circuit1():
    qml.PauliZ(0)
    qml.PauliZ(1)
    #qml.PauliZ(2)
    return qml.state()

# as shown in https://pennylane.ai/qml/demos/tutorial_qubit_rotation/
# a rotation on X by angle x and a rotation on Y by angle y = cos x cos y
@qml.qnode(dev)
def twoRot(x, y):
    qml.RX(x, 0)
    qml.RY(y, 0)
    qml.PauliZ(0)
    return qml.state()

@qml.qnode(dev)
def twoRotWithHad(x, y):
    qml.RX(x, 0)
    qml.RY(y, 0)
    qml.Hadamard(0)
    return qml.expval(qml.PauliZ(0))

@qml.qnode(dev)
def had_exp():
    qml.Hadamard(0)
    return qml.expval(qml.PauliZ(0))


@qml.qnode(dev)
def had_sample():
    qml.Hadamard(0)
    return qml.sample(qml.PauliZ(0))

@qml.qnode(dev) 
def circuit_entangle():
    # entangle qubits
    qml.PauliX(wires=0)
    #qml.CNOT(wires=[0, 1])
    # mess with qubit 0   
    #qml.Hadamard(wires=0)
    # return qubit 1 
    return qml.expval(qml.PauliZ(1))

# ---------------------------------------------------------------------------

# we expect 2**wires number of elements in the state vector
# for 1 wire (qubit) we expect to see [1.+0.j 0.+0.j], the ground state |0> 
# for 2 wires we expect to see [1.+0.j 0.+0.j 0.+0.j 0.+0.j], the |0> state
# for 3 wires we expect to see 
#   [1.+0.j 0.+0.j 0.+0.j 0.+0.j 0.+0.j 0.+0.j 0.+0.j 0.+0.j], the |0> state
#state = getInitialState()
#print(state)
#print()
#print(qml.draw(circuit1)())
#print(circuit1())
#print()
#print(qml.draw(circuit_entangle)())
#print(circuit_entangle())

print(getInitialState())
print(pz())
print(pz_exp())
print(pz_sample())
print(flip())
print(flip_pz())
print(flip_pz_exp())
print(flip_pz_sample())
print(had_exp())
print(had_sample())
#print(twoRot(np.pi, np.pi))         # expect cos pi cos pi = 1
#print(twoRot(np.pi/2, np.pi/2))     # expect cos pi/2 cos pi/2 = 0

#print(twoRot(np.pi/4, np.pi/4))     # expect cos pi/4 cos pi/4 = 0.5
#print(twoRotWithHad(np.pi/4, np.pi/4))     # still 0.5
  

