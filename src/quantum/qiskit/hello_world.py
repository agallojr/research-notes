from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli 
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import Sampler


# Create a new circuit with two qubits (first argument) and two classical
# bits (second argument)
qc = QuantumCircuit(2, 2)
 
# Add a Hadamard gate to qubit 0
qc.h(0)
 
# Perform a controlled-X gate on qubit 1, controlled by qubit 0
qc.cx(0, 1)
 
# Return a drawing of the circuit using MatPlotLib ("mpl"). This is the
# last line of the cell, so the drawing appears in the cell output.
# Remove the "mpl" argument to get a text drawing.
print(qc.draw())

ZZ = Pauli('ZZ')
ZI = Pauli('ZI')
IZ = Pauli('IZ')
XX = Pauli('XX')
XI = Pauli('XI')
IX = Pauli('IX')

service = QiskitRuntimeService(channel="ibm_quantum", token="<token>")
backend = service.get_backend("ibmq_qasm_simulator")
pm = generate_preset_pass_manager(backend=backend)
isa_circuit = pm.run(qc)
ZZ = ZZ.apply_layout(isa_circuit.layout)
ZI = ZI.apply_layout(isa_circuit.layout)
ZI = ZI.apply_layout(isa_circuit.layout)
IZ = IZ.apply_layout(isa_circuit.layout)
XX = XX.apply_layout(isa_circuit.layout)
IX = IX.apply_layout(isa_circuit.layout)
XI = XI.apply_layout(isa_circuit.layout)

job = Sampler(backend).run(isa_circuit)
print(f"job id: {job.job_id()}")
result = job.result()
print(result)
