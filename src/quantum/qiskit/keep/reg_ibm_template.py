from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(channel="ibm_quantum", 
    token="<MY_IBM_QUANTUM_TOKEN>", 
    overwrite=True,
    set_as_default=True)

