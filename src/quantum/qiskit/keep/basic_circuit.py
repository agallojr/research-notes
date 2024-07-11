from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import Sampler


# Create a new circuit with two qubits (first argument) and two classical
# bits (second argument)
qc = QuantumCircuit(12, 2)
# Add a Hadamard gate to qubit 0
qc.h(0)
 
# Perform a controlled-X gate on qubit 1, controlled by qubit 0
qc.cx(0, 1)

qc.measure_all()
 
service = QiskitRuntimeService()
backend = service.backend("ibmq_qasm_simulator")
job = Sampler(backend).run(qc)
print(f"job id: {job.job_id()}")
result = job.result()
print(result)
