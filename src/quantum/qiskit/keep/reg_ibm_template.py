from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(channel="ibm_quantum", 
    token="880645434224203fa7bfdeb925640baa205e0dd8d6a2188659c906f14f1a666b262a3ccf1bfd71e90d52cfc3008b4fb051f0dd30ec50e869bd2f0ef829907cba", 
    overwrite=True,
    set_as_default=True)

