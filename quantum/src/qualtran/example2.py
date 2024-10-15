
from qualtran import Register, QBit, Bloq, CompositeBloq, Signature 
import attrs
from qualtran import drawing 
from qualtran.bloqs.basic_gates import CNOT 
    

cnot = CNOT()
with open("alg2.svg", "w") as text_file:
    text_file.write(drawing.graphviz.PrettyGraphDrawer(cnot).get_svg().data)

# try to convert to a circuit
from qualtran.cirq_interop import CirqGateAsBloq
#print(CompositeBloq.to_cirq_circuit(cnot))
print(Bloq.as_cirq_op(cnot))




