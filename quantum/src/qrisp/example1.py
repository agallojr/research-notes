
from qrisp import QuantumVariable
qv = QuantumVariable(5)

from qrisp import h, z, cx
h(qv[0])
z(qv)
cx(qv[0], qv[3])

print(qv.qs)


