from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qc_grader.challenges.qgss_2024 import grade_lab2_ex1, grade_lab2_ex2, \
    grade_lab2_ex3, grade_lab2_ex4
from qiskit.circuit import Parameter
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import numpy as np
from qiskit.primitives.containers.bindings_array import BindingsArray

service = QiskitRuntimeService()
backend = AerSimulator.from_backend(service.backend("ibm_osaka"))

BACKEND = backend
PATH_ANSWER = [ 0, 1, 2, 3, 4, 5, 6, 7, 8 ] 

# grade part 1
#grade_lab2_ex1(PATH_ANSWER, BACKEND)

LAYER_1_ANSWER = [ (1, 0), (2, 3), (5, 4), (6, 7) ]
LAYER_2_ANSWER = [ (2, 1), (3, 4), (6, 5), (7, 8) ]

# grade part 2
#grade_lab2_ex2(LAYER_1_ANSWER, LAYER_2_ANSWER, PATH_ANSWER, BACKEND)

CIRC_1_ANSWER = QuantumCircuit(9)
CIRC_1_ANSWER.ecr(1, 0)
CIRC_1_ANSWER.ecr(2, 3)
CIRC_1_ANSWER.ecr(5, 4)
CIRC_1_ANSWER.ecr(6, 7)

CIRC_2_ANSWER = QuantumCircuit(9)
CIRC_2_ANSWER.ecr(2, 1)
CIRC_2_ANSWER.ecr(3, 4)
CIRC_2_ANSWER.ecr(6, 5)
CIRC_2_ANSWER.ecr(7, 8)

# grade part 3
#grade_lab2_ex3(CIRC_1_ANSWER, LAYER_1_ANSWER, "ecr", BACKEND)
#grade_lab2_ex3(CIRC_2_ANSWER, LAYER_2_ANSWER, "ecr", BACKEND)



def eplg_circuit(num_qubits: int, depth: int, layer: QuantumCircuit, qubits: tuple[int, ...]) -> QuantumCircuit:
    if depth % 2 != 0:
        raise ValueError(f"The depth must be even, got {depth}")

    def parameters():
        _depth = 0
        while True:
            for zi in range(3):
                for q in range(num_qubits):
                    yield Parameter(f"d{_depth}_q{q}_z{zi}")
            _depth += 1
    _parameters = parameters()

    circ = QuantumCircuit(num_qubits)

    def _1q_layer():
        for j in range(3):
            for k in qubits:
                circ.rz(next(_parameters), k)
            if j == 2:
                continue
            circ.sx(qubits)

    for _depth in range(depth // 2):
        circ.barrier(qubits)
        _1q_layer()
        circ.barrier(qubits)
        circ.compose(layer, inplace=True)
    circ.barrier(qubits)
    _1q_layer()
    circ.barrier(qubits)
    
    # Assuming mirroring is fine
    circ = circ.compose(circ.inverse())

    circ.measure_active()

    pm = generate_preset_pass_manager(basis_gates=["ecr", "sx", "rz"], optimization_level=0)
    circ = pm.run(circ)

    circ.metadata["layer_depth"] = depth
    circ.metadata["qubits"] = qubits
    circ.metadata["num_qubits"] = num_qubits

    return circ

def get_clifford_rz_samples(
    circ: QuantumCircuit,
    num_samples: int,
    rng: np.random.Generator,
) -> BindingsArray:
    """Uniformly sample the Rz parameters in a `QuantumCircuit`
    from -pi, -pi/2, 0, +pi/2, +pi.
    """

    _allowed_ops = {'rz', 'sx', 'sxdg', 'ecr', 'barrier', 'measure'}
    if (_other := set(circ.count_ops().keys()) - _allowed_ops):
        raise ValueError(f"Circuit must only contain ops: {_allowed_ops}, got {_other}")

    sampled_pars = rng.integers(-2, 3, size=(num_samples, len(circ.parameters))) * (np.pi/2)

    return BindingsArray({
        tuple(circ.parameters): sampled_pars
    })


example_circuit_1 = eplg_circuit(
    num_qubits=BACKEND.num_qubits,
    depth=4,
    layer=CIRC_1_ANSWER,
    qubits=PATH_ANSWER,
)

example_circuit_2 = eplg_circuit(
    num_qubits=BACKEND.num_qubits,
    depth=4,
    layer=CIRC_2_ANSWER,
    qubits=PATH_ANSWER,
)

num_samples = 10
ARRAY_1_ANSWER = get_clifford_rz_samples(
    circ=example_circuit_1,
    num_samples=num_samples,
    rng=np.random.default_rng(42))


# grade part 4 
# grade_lab2_ex4(ARRAY_1_ANSWER, example_circuit_1, num_samples)

