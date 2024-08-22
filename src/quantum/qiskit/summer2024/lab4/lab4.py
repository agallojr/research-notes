from qiskit.circuit import QuantumCircuit, Parameter
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler import CouplingMap
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.synthesis import LieTrotter
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.options import EstimatorOptions,\
    DynamicalDecouplingOptions
from qiskit_ibm_runtime import EstimatorV2, Batch

import numpy as np
import matplotlib.pyplot as plt
import json

from qiskit.providers.fake_provider import GenericBackendV2


from qiskit import transpile, QuantumCircuit
from qiskit.circuit import Gate
from qiskit.converters import circuit_to_dag
from qiskit.transpiler import CouplingMap, StagedPassManager, PassManager, AnalysisPass, TransformationPass
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.transpiler.preset_passmanagers.common import generate_unroll_3q, generate_embed_passmanager
from qiskit.quantum_info import hellinger_fidelity
from qiskit.providers.basic_provider import BasicSimulator
from qiskit.dagcircuit import DAGCircuit
from qiskit_ibm_runtime.fake_provider import FakeTorino

# Transpiler Passes
## Layout passes
from qiskit.transpiler.passes.layout.csp_layout import CSPLayout
from qiskit.transpiler.passes.layout.dense_layout import DenseLayout
from qiskit.transpiler.passes.layout.sabre_layout import SabreLayout
from qiskit.transpiler.passes.layout.vf2_layout import VF2Layout
from qiskit.transpiler.passes.layout.trivial_layout import TrivialLayout

## Routing passes
from qiskit.transpiler.passes.routing.basic_swap import BasicSwap
from qiskit.transpiler.passes.routing.lookahead_swap import LookaheadSwap
from qiskit.transpiler.passes.routing.sabre_swap import SabreSwap
from qiskit.transpiler.passes.routing.stochastic_swap import StochasticSwap
from qiskit.transpiler.passes.routing.star_prerouting import StarPreRouting

## Synthesis passes (passes for the translation stage)
from qiskit.circuit import SessionEquivalenceLibrary
from qiskit.circuit.equivalence_library import SessionEquivalenceLibrary
from qiskit.transpiler.passes.basis.basis_translator import BasisTranslator
from qiskit.transpiler.passes.synthesis.high_level_synthesis import HighLevelSynthesis
### The next pass could also be considered an optimization pass.
from qiskit.transpiler.passes.synthesis.unitary_synthesis import UnitarySynthesis

## Optimization passes
from qiskit.transpiler.passes.optimization.collect_1q_runs import Collect1qRuns
from qiskit.transpiler.passes.optimization.collect_2q_blocks import Collect2qBlocks
from qiskit.transpiler.passes.optimization.consolidate_blocks import ConsolidateBlocks
from qiskit.transpiler.passes.optimization.commutative_cancellation import CommutativeCancellation

import matplotlib.pyplot as plt
import random 

from qc_grader.challenges.qgss_2024 import grade_lab4_ex1, grade_lab4_ex2, \
    grade_lab4_ex3, grade_lab4_ex4, grade_lab4_ex5, grade_lab4_ex6

# Define system parameters

num_spins = 12
anisotropy = 1.
h = 1.
dt = Parameter('δt')

lattice_map = CouplingMap.from_ring(num_spins, bidirectional=False)

edgelist = lattice_map.graph.edge_list()
#print(edgelist)
hamlist = []

for edge in edgelist:
    hamlist.append(("XX", edge, 1.))
    hamlist.append(("YY", edge, 1.))
    hamlist.append(("ZZ", edge, anisotropy))

for qubit in lattice_map.physical_qubits:
    hamlist.append(("X", [qubit], h))

#hamiltonian = SparsePauliOp.from_sparse_list(hamlist, num_qubits=num_spins)
#print(hamiltonian)

def build_hamiltonian(num_spins, anisotropy, h):  
    lattice_map = CouplingMap.from_line(num_spins, bidirectional=False)
    edgelist = lattice_map.graph.edge_list()
    hamlist = []
    for edge in edgelist:
        hamlist.append(("XX", edge, 1.))
        hamlist.append(("YY", edge, 1.))
        hamlist.append(("ZZ", edge, anisotropy))

    for qubit in lattice_map.physical_qubits:
        hamlist.append(("XX", [qubit], h))

    hamiltonian = SparsePauliOp.from_sparse_list(hamlist, num_qubits=num_spins)
    return hamiltonian


#print(build_hamiltonian(num_spins, anisotropy, h))

#grade_lab4_ex1(build_hamiltonian)

#**************************************************************

hamiltonian = build_hamiltonian(num_spins, anisotropy, h)

time_evolution_operator = PauliEvolutionGate(hamiltonian, time=dt)
trotter_factory = LieTrotter(reps=4)
evolution_circuit = trotter_factory.synthesize(time_evolution_operator)
evolution_circuit.decompose()
#plt.show()
z_observables = [ SparsePauliOp.from_sparse_list([('Z', [i], 1.)], \
    num_qubits=num_spins) for i in range(num_spins) ] 
#print(z_observables)

def build_layered_hamiltonian(num_spins, anisotropy, h):
    lattice_map = CouplingMap.from_line(num_spins, bidirectional=False)
    edgelist = lattice_map.graph.edge_list()
    even_hamlist = []
    odd_hamlist = []
    hamlist = []
    for edge in edgelist:
        if edge[0] % 2 == 0:
            even_hamlist.append(("XX", edge, 1.))
            even_hamlist.append(("YY", edge, 1.))
            even_hamlist.append(("ZZ", edge, anisotropy))
        else:
            odd_hamlist.append(("XX", edge, 1.))
            odd_hamlist.append(("YY", edge, 1.))
            odd_hamlist.append(("ZZ", edge, anisotropy))

    hamlist = even_hamlist
    for qubit in range(num_spins):
        hamlist.append(("X", [qubit], h))
    hamlist += odd_hamlist
    hamiltonian = SparsePauliOp.from_sparse_list(hamlist, num_qubits=num_spins)
    return hamiltonian

hamiltonian = build_layered_hamiltonian(num_spins, anisotropy, h)

#grade_lab4_ex2(build_layered_hamiltonian)

#**************************************************************

# Your code goes here

service = QiskitRuntimeService()
backend = service.backend("ibm_osaka")
#backend = AerSimulator.from_backend(service.backend("ibm_osaka"))
#backend = GenericBackendV2(num_spins)
#cm = CouplingMap.from_line(num_spins, bidirectional=False)
#pm_opt = StagedPassManager()
#pm_opt.layout = PassManager()
#pm_opt.layout += TrivialLayout(cm)

pass_manager = generate_preset_pass_manager(2, backend=backend)
# Run the pass manager on `evolution_circuit` 
isa_circuit = pass_manager.run(evolution_circuit)
#print(isa_circuit)
#isa_circuit.layout.input_qubit_mapping = cm._qubit_list
#print(z_observables)

#for observable in z_observables:
#    #print(observable)
#    print(observable.apply_layout(isa_circuit.layout))

isa_z_obs = [
    observable.apply_layout(isa_circuit.layout) for observable in z_observables
]

#print(isa_z_obs)
#grade_lab4_ex3(backend, isa_circuit, isa_z_obs)


#**************************************************************


dd_options = DynamicalDecouplingOptions(enable=True, sequence_type="XpXm")
options = EstimatorOptions(dynamical_decoupling=dd_options)
options.resilience.zne_mitigation = True


# Exercise 4: Create the set of transpiled time evolution circuits and observables for each
#  of the phases and values of h to investigate.
# Hint: list comprehension will make this much simpler to approach

dt = Parameter('δt')
dt_val = [5*np.pi/2.]
h_vals = np.linspace(0., np.pi/2, 12)
anisotropies = {"Anisotropic":-5., "XXX":1}
num_spins = 50

# Dictionaries to use for exercise submission
hamiltonians = {}
hamiltonians["Anisotropic"] = list()
hamiltonians["XXX"] = list()
time_evolution_operators = {}
time_evolution_operators["Anisotropic"] = list()
time_evolution_operators["XXX"] = list()
trotter_circuits = {}
isa_circuits = {}
isa_circuits["Anisotropic"] = list()
isa_circuits["XXX"] = list()
isa_z_observables = {}
isa_z_observables["Anisotropic"] = list()
isa_z_observables["XXX"] = list()

# Loop over each phase of the heisenberg system
for phase, anisotropy in anisotropies.items():
    # For each anisotropy value you'll need to loop over all values from h_vals
    for h in h_vals:
        # At each value of h, you'll need to
        # 1. Generate the associated hamiltonian
        ham = build_layered_hamiltonian(num_spins, anisotropy, h)
        hamiltonians[phase].append(ham)
        # 2. Create the time evolution operator
        tevop = PauliEvolutionGate(ham, time=dt)
        time_evolution_operators[phase].append(tevop)
        # 3. Generate the time evolution circuit
        trotter_factory = LieTrotter(reps=4)
        trotter_factory.settings["time"] = dt
        evolution_circuit = trotter_factory.synthesize(tevop)
        evolution_circuit.decompose()
        # 4. Transpile the circuit
        isa_circuit = pass_manager.run(evolution_circuit)
        isa_circuits[phase].append(isa_circuit)
        # 5. Apply the layout of the transpiled circuit to the observables
        z_observables = [ SparsePauliOp.from_sparse_list([('Z', [i], 1.)], \
            num_qubits=num_spins) for i in range(num_spins) ] 
        isa_z_obs = [
            observable.apply_layout(isa_circuit.layout) \
                for observable in z_observables
        ]
        isa_z_observables[phase].append(isa_z_obs)
 



#grade_lab4_ex4(hamiltonians,
#              time_evolution_operators,
#              isa_circuits,
#              isa_z_observables)


#**************************************************************

all_z_obs_pubs = {}
all_z_obs_pubs["Anisotropic"] = list()
all_z_obs_pubs["XXX"] = list()
for phase, circuits in isa_circuits.items():
    observables = isa_z_observables[phase]
    for circuit, observable in zip(circuits, observables):
        pub = (circuit, observable, dt_val)
        all_z_obs_pubs[phase].append(pub)

#grade_lab4_ex5(all_z_obs_pubs)

#**************************************************************

# Exercise 6: Use the `Batch` context to run your circuits
all_z_obs_jobs = {}
all_z_obs_jobs["Anisotropic"] = []
all_z_obs_jobs["XXX"] = []

print("Submitting jobs...")
print("all_z_obs_pubs", all_z_obs_pubs)
print("count A", len(all_z_obs_pubs["Anisotropic"]))
print("count xxx", len(all_z_obs_pubs["XXX"]))


with Batch(backend=backend) as batch:
    # Print information about the session
    print(f"Session ID: {batch.session_id}")
    print(f"Backend: {batch.backend()}")
    # Instantiate an estimator primitive
    estimator = EstimatorV2(session=batch, options=options)
    for phase, pub in all_z_obs_pubs.items():
        job = estimator.run(pubs=pub)
        all_z_obs_jobs[phase].append(job.job_id())

#print(all_z_obs_jobs)

# Store job ids into a dictionary and save them as a json file
fname = "lab4_ex6.json"
with open(fname, 'w') as file:
   json.dump(all_z_obs_jobs, file)

# Uncomment the below line if you were unable to run this on hardware
#fname = "skip-question"

grade_lab4_ex6(fname)


