from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix
from qiskit.visualization import plot_state_qsphere, plot_state_city
import matplotlib.pyplot as plt
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime import Session
from qiskit_aer import AerSimulator 
import time

# make the circuit 
circ = QuantumCircuit(4)
circ.h(0)
circ.h(1)
circ.h(2)
circ.h(3)
circ.cx(0, 1)
circ.cx(0, 2)
circ.cx(0, 3)
#circ.cx(1, 2)
#circ.cx(1, 3)
#circ.cx(1, 0)
#circ.cx(2, 3)   
#circ.cx(2, 0)
#circ.cx(2, 1)
#circ.cx(3, 0)
#circ.cx(3, 1)
#circ.cx(3, 2)



circ.draw(output="mpl")
state = Statevector(circ)
plot_state_qsphere(state, show_state_phases=False)
den = DensityMatrix(circ)
plot_state_city(den)
plt.show()

circ.measure_all()

# Run the sampler job locally using FakeManilaV2
fake_manila = FakeManilaV2()
pm = generate_preset_pass_manager(backend=fake_manila, optimization_level=1)
isa_qc = pm.run(circ)
 
# You can use a fixed seed to get fixed results.
options = {"simulator": {"seed_simulator": 42}}
sampler = Sampler(mode=fake_manila, options=options)
 
result = sampler.run([isa_qc]).result()
print(result)

aer_sim = AerSimulator()
pm = generate_preset_pass_manager(backend=aer_sim, optimization_level=1)
isa_qc = pm.run(circ)
with Session(backend=aer_sim) as session:
    sampler = Sampler(mode=session)
    result = sampler.run([isa_qc]).result()
    print(f" > Counts: {result[0].data.meas.get_counts()}")



