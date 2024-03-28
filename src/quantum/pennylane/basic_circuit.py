import pennylane as qml
import numpy as np        # be aware that pennylane also has its own numpy wrapper...

# ---------------------------------------------------------------------------
# setups for various quantum computers & simulators, assumes all these plugins have 
# been installed via pip

# *) pennylane default simulator 
#dev = qml.device('default.qubit', wires=2, shots=1000)

# *) pennylane lightning (fast C++ impl) simulator
dev = qml.device('lightning.qubit', wires=2, shots=1000)

# *) pennylane lightning gpu simulator based on CUDA - results in fallback to 
# default.qubit on unsupported hardware cuz cuda
#dev = qml.device('lightning.gpu', wires=2, shots=1000, mpi=True)

# *) pennylane kokkos-based simulator
#dev = qml.device("lightning.kokkos", wires=2, shots=1000)

# *) AWS Braket simulator
#dev = qml.device('braket.local.qubit', wires=2, shots=1000)

# *) AWS Braket cloud service - a real quantum computer!
# set environment variables AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
#arn = "arn:aws:braket:us-east-1::device/qpu/ionq/Aria-1"  # physical quantum computer
#s3 = ("agallojr", "arn:aws:s3:::agallojr")         # bucket to hold results
#dev = qml.device('braket.aws.qubit',
#                 device_arn=arn, 
#                 #s3_destination_folder=s3, 
#                 wires=2, 
#                 shots=10)

# *) IBM aer simulator
#dev = qml.device('qiskit.basicaer', wires=2, shots=1000)

# *) IBM Quantum Platform - a real quantum computer!
# set the IBMQX_TOKEN environment variable with the IBM user's token
#import os
#from qiskit_ibm_provider import IBMProvider
#IBMProvider.save_account(os.getenv('IBMQX_TOKEN'), overwrite=True)
#dev = qml.device('qiskit.ibmq', 
#                 backend="ibm_kyoto",    # one of several machines available
#                 ibmqx_token=os.getenv('IBMQX_TOKEN'),
#                 hub='ibm-q', group='open', project='main',
#                 wires=2, shots=100)


# ---------------------------------------------------------------------------

# a simple circuit wrapped as a pennylane qnode on the specified device
@qml.qnode(dev) 
def circuit1(x, y):
    qml.RZ(x, wires=0)
    qml.CNOT(wires=[0,1])
    qml.RY(y, wires=1)
    return qml.expval(qml.PauliZ(1))

# ---------------------------------------------------------------------------

# we're expecting to converge to a value around 0.7, but with a few shots (10) we can't
# predict what we'll see... might be 1.0 even... these lines of code will not run on 
# the quantum computer itself, but will run in conjunction with a local simulator.
print(circuit1(np.pi/4, 0.7))
print(qml.draw(circuit1)(np.pi/4, 0.7))



