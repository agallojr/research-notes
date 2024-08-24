from qiskit_ibm_runtime import QiskitRuntimeService

with open('token.txt', 'r') as file:
    token_data = file.read().rstrip()

QiskitRuntimeService.save_account(channel="ibm_quantum", 
    token=token_data, 
    overwrite=True,
    set_as_default=True)

