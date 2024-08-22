# import of required libraries and modules
from qc_grader.challenges.qgss_2024 import *

import matplotlib.pyplot as plt

from qiskit.converters import circuit_to_dag
from math import pi
from qiskit.circuit import Qubit
from qiskit.circuit.library import QFT
from qiskit.providers.fake_provider import GenericBackendV2, generic_backend_v2
generic_backend_v2._NOISE_DEFAULTS["cx"] = (5.99988e-06, 6.99988e-06, 1e-5, 5e-3)

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


#Hint: see https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.QuantumCircuit
def get_qc_characteristics(qc):
    # Your work goes here!
    # determine the quantum circuit depth of `qc` and assign it to `depth`
    depth = qc.depth()
    # determine the number of qubits in `qc` and assign it to `num_qubits`    
    num_qubits = qc.num_qubits
    # determine the operations in `qc` and assign it to `ops`
    ops = qc.count_ops()
    # determine the number of n-qubit operations (with n larger than 1) in `qc` and assign it to `num_multi_qubit_ops`, 
    num_multi_qubit_ops = 0
    for d in qc.data:
        if d.operation.num_qubits > 1:
            num_multi_qubit_ops += 1
    # do not modify the next line
    return {"depth":depth, "num_qubits":num_qubits, "ops":ops, "num_multi_qubit_ops": num_multi_qubit_ops}  



# get an abstract quantum circuit from Qiskit's library of circuits 
num_qubits = 10
qc = QFT(num_qubits, do_swaps=False)
#qc.draw(output="mpl")
#plt.show()

# grade part 1
#grade_lab1_ex1(get_qc_characteristics)

#********************************************************


# print quantum circuit characteristics
def print_qc_characteristics(qc):
    characteristics = get_qc_characteristics(qc)
    print("Quantum circuit characteristics")
    print("  Depth:", characteristics['depth'])
    print("  Number of qubits:", characteristics['num_qubits'])   
    print("  Operations:", dict(characteristics['ops']))
    print("  Number of multi-qubit Operations:", characteristics['num_multi_qubit_ops'])
    

#print_qc_characteristics(qc)

qc_dec = qc.decompose()
get_qc_characteristics(qc_dec)
#qc_dec.draw(output="mpl", fold=-1)
#plt.show()


# transpile the circuit
backend = GenericBackendV2(num_qubits)
#print("Supported basis gates:", backend.operation_names)
#qc_synth = generate_preset_pass_manager(2, backend=backend).run(qc)
#qc_synth.draw(output="mpl", fold=-1)
#plt.show()

#print_qc_characteristics(qc_synth)

# assign a 10-qubit linear `CouplingMap` to the variable cm
#print(backend.coupling_map)
cm = CouplingMap([ (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 8), (8, 7), (7, 6), (6, 5), (5, 4), (4, 3), (3, 2), (2, 1), (1, 0) ])

# add your transpiled quantum circuit to the next line
#qc_routed = generate_preset_pass_manager(2, coupling_map=cm).run(qc)

# grade part 2
#grade_lab1_ex2(qc_routed)

#********************************************************
#print("start of part 3")
#print(qc)   # shows a 10-qubit QFT gate 
#cm = backend.coupling_map

# transpile in stages 
pm_staged = StagedPassManager()
# replace the n-qubit QFT operation with its decomposition in two-qubit gates
pm_staged.init = generate_unroll_3q(None)
# initialize the layout stage with an empty pass manager
pm_staged.layout = PassManager()
# set a trivial initial layout, each qubit in the quantum circuit with index i 
# is mapped to the physical qubit on a device with the same index
pm_staged.layout += TrivialLayout(cm)

# do not modify the next line
pm_staged.layout += generate_embed_passmanager(cm)

# Your work goes here!
pm_staged.routing = PassManager(SabreSwap(cm))



#pm_staged.optimization = PassManager()
#pm_staged.optimization += Collect2qBlocks()
#pm_staged.optimization += ConsolidateBlocks()
#pm_staged.optimization += \
#    UnitarySynthesis(basis_gates = backend.operation_names)
#pm_staged.optimization += CommutativeCancellation()

#for t in pm_staged._tasks:
#    print(t)

#qc_routed = pm_staged.run(qc)
#print_qc_characteristics(qc_routed)

#grade_lab1_ex3(pm_staged)

#********************************************************

#print(pm_staged.expanded_stages)

pm_staged.translation =  \
    PassManager(BasisTranslator(SessionEquivalenceLibrary,\
        backend.operation_names))
pm_staged.translation += HighLevelSynthesis()

#for t in pm_staged._tasks:
#    print(t)

qc_routed_synth = pm_staged.run(qc)
#print_qc_characteristics(qc_routed_synth)

#grade_lab1_ex4(pm_staged)

#********************************************************

def noisy_sim(qc, backend):
    # We add measurement operations to the input quantum circuit and then run it on the specified backend
    # A GenericBackendV2 automatically constructs a default model of the expected noise processes,
    # so backend.run would return noisy simulation results
    return backend.run(qc.measure_all(inplace=False), shots=7 * 1024).result().get_counts()

qk_qc = generate_preset_pass_manager(2, backend=backend).run(qc)
own_transpiler_sim = noisy_sim(qc_routed_synth, backend)
qiskit_transpiler_sim = noisy_sim(qk_qc, backend)
reference_sim = noisy_sim(transpile(qc.decompose(), backend=backend), BasicSimulator())

print("Own transpiler fidelity", round(hellinger_fidelity(own_transpiler_sim, reference_sim), 4))
print("Qiskit transpiler fidelity", round(hellinger_fidelity(qiskit_transpiler_sim, reference_sim), 4))


pm_opt = StagedPassManager()
# Select pass managers and passes for these five stages as you see suitable, note: not every stage must contain a pass.
# Passes are documented at https://docs.quantum.ibm.com/api/qiskit/transpiler_passes

# Replace the n-qubit QFT operation with its decomposition in two-qubit gates
pm_opt.init = generate_unroll_3q(None)
# Initialize the layout stage with an empty pass manager
pm_opt.layout = PassManager()
# See the first cells in this notebook or
#   https://github.com/Qiskit/qiskit/tree/main/qiskit/transpiler/passes/layout for potential layouting passes
pm_opt.layout += TrivialLayout(cm)
# See the first cells in this notebook or
#   https://github.com/Qiskit/qiskit/tree/main/qiskit/transpiler/passes/routing for potential routing passes
pm_opt.pre_routing = PassManager(StarPreRouting()) 
pm_opt.routing = PassManager(SabreSwap(cm))
# See the first cells in this notebook or
#   https://github.com/Qiskit/qiskit/tree/main/qiskit/transpiler/passes/synthesis for potential translation passes
pm_opt.translation = \
    PassManager(BasisTranslator(SessionEquivalenceLibrary,\
        backend.operation_names))
pm_opt.translation += HighLevelSynthesis()
# See the first cells in this notebook or
#   https://github.com/Qiskit/qiskit/tree/main/qiskit/transpiler/passes/optimization for potential optimization passes
pm_opt.optimization = PassManager()
pm_opt.optimization += Collect2qBlocks()
pm_opt.optimization += ConsolidateBlocks()
pm_opt.optimization += \
    UnitarySynthesis(basis_gates = backend.operation_names)
pm_opt.optimization += CommutativeCancellation()

# scheduling is not needed in this lab - we will not run the quantum circuit on a real device
# pm_opt.scheduling = None

# do not modify the next line
#pm_opt.layout += generate_embed_passmanager(cm)

#qc_opt = pm_opt.run(qc)

#grade_lab1_ex5(pm_opt)

#********************************************************

class GatesPerQubit(AnalysisPass):

    def is_transformation_pass(self):
        return False
    def is_analysis_pass(self):
        return True

    def run(self, dag: DAGCircuit):
        one_q_op = dict()
        two_q_op = dict()       
        for q in dag.qubits:
            one_q_op[q] = 0
            two_q_op[q] = 0
        for dop in dag.op_nodes():
            if (dop.op.num_qubits == 1):
                one_q_op[dop.qargs[0]] += 1
            elif (dop.op.num_qubits == 2):
                two_q_op[dop.qargs[0]] += 1
                two_q_op[dop.qargs[1]] += 1
        self.property_set["one_q_op"] = one_q_op
        self.property_set["two_q_op"] = two_q_op
        return


qc = QFT(4, do_swaps=False)
qc = generate_preset_pass_manager(2, backend=backend).run(qc)
gpq = GatesPerQubit()
gpq(qc)

#print("single-qubit gates on qubit", gpq.property_set["one_q_op"])
#print("two-qubit gates on qubit", gpq.property_set["two_q_op"])

#grade_lab1_ex6(GatesPerQubit)


#****************************************************************

qc = QFT(4, do_swaps=False)
qc = generate_preset_pass_manager(2, backend=backend).run(qc)
gpq = GatesPerQubit()
gpq(qc)
print("single-qubit gates on qubit", gpq.property_set["one_q_op"])
print("two-qubit gates on qubit", gpq.property_set["two_q_op"])
#qc.draw(fold=-1, idle_wires=False)

pg = Gate('Peres', 3, params=[], label='PG')
qc_pg = QuantumCircuit(3)
qc_pg.append(pg, [0, 1, 2])
#qc_pg.draw()

def get_qc_in(nq):
    # QFT circuit, feel free to use a previously defined pass manager for the QFT circuit
    qc_qft = QFT(nq, do_swaps=False)
    # part of the circuit including the Peres gate
    qc_inner = QuantumCircuit(nq)
    for i in range(1, nq - 1):
        qc_inner.append(pg, [nq - i - 2, nq - i - 1, nq - 1])

    qc_in = QuantumCircuit(nq)
    # add QFT circuit to qc_in
    qc_in.compose(qc_qft, range(nq), inplace=True)

    # perform swap gates
    for i in range(nq // 2):
        qc_in.cx(i, nq - i - 1)
        qc_in.cx(nq - i - 1, i)
        qc_in.cx(i, nq - i - 1)

    qc_in.rz(pi, nq - 1)
    # add circuit with peres gates
    qc_in.compose(qc_inner, range(nq), inplace=True)

    # perform swap gates
    for i in range(nq // 2):
        qc_in.cx(i, nq - i - 1)
        qc_in.cx(nq - i - 1, i)
        qc_in.cx(i, nq - i - 1)
    # add inverse QFT circuit
    qc_in.compose(qc_qft.inverse(), range(nq), inplace=True)
    return qc_in

nq = 5
qc_in = get_qc_in(nq)
#qc_in.draw(fold=-1)

class PeresGateTranslation(TransformationPass):
    def get_peres_decomposition(self):
        qcsx = QuantumCircuit(2)
        qcsx.rz(pi / 4, 0)
        qcsx.rz(pi / 2, 1)
        qcsx.sx(1)
        qcsx.rz(pi / 2, 1)
        qcsx.cx(0, 1)
        qcsx.rz(-pi / 4, 1)
        qcsx.cx(0, 1)
        qcsx.rz(3 * pi / 4, 1)
        qcsx.sx(1)
        qcsx.rz(pi / 2, 1)

        qcsx_inv = QuantumCircuit(2)
        qcsx_inv.rz(pi / 4, 1)
        qcsx_inv.cx(0, 1)
        qcsx_inv.rz(-pi / 4, 1)
        qcsx_inv.cx(0, 1)
        qcsx_inv.rz(pi / 2, 0)
        qcsx_inv.rz(pi / 2, 1)
        qcsx_inv.cx(0, 1)
        qcsx_inv.rz(pi / 2, 1)
        qcsx_inv.sx(1)
        qcsx_inv.rz(-3 * pi / 4, 1)
        qcsx_inv.sx(1)
        qcsx_inv.cx(0, 1)
        qcsx_inv.sx(1)
        qcsx_inv.rz(-3 * pi / 4, 1)
        qcsx_inv.sx(1)
        qcsx_inv.rz(-3 * pi / 4, 1)
        qcsx_inv.cx(0, 1)
        qcsx_inv.rz(-pi / 4, 1)
        qcsx_inv.cx(0, 1)
        qcsx_inv.rz(pi / 4, 0)

        qc_dec = QuantumCircuit(3)
        qc_dec.cx(0, 1)
        qc_dec.cx(1, 0)
        qc_dec.cx(0, 1)
        qc_dec.compose(qcsx, [1, 2], inplace=True)
        qc_dec.cx(0, 1)
        qc_dec.cx(1, 0)
        qc_dec.cx(0, 1)
        qc_dec.compose(qcsx, [1, 2], inplace=True)
        qc_dec.cx(0, 1)
        qc_dec.compose(qcsx_inv, [1, 2], inplace=True)
        qc_dec.cx(0, 1)
        qc_dec.cx(0, 1)
        return qc_dec


    def is_transformation_pass(self):
        return True
    def is_analysis_pass(self):
        return False
    
    def run(self, dag: DAGCircuit):
        for node in dag.op_nodes():  # Remove op_name argument
            if node.name == 'Peres':  # Filter nodes by name manually
                qxlate = self.get_peres_decomposition()
                dag.substitute_node_with_dag(node, circuit_to_dag(qxlate))
        return dag


#pm_opt = generate_preset_pass_manager(2, backend=backend)
pm_opt = StagedPassManager()
pm_opt.translation = PassManager(PeresGateTranslation())
print("*****")
for t in pm_opt._tasks:
    print(t)


#dag = qiskit.converters.circuit_to_dag(self.get_peres_decomposition())

qc_pg = pm_opt.run(qc_in)


grade_lab1_ex7(PeresGateTranslation, pg)






