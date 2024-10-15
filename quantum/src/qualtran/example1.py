
from qualtran import Register, QBit, Bloq, Signature 
import attrs
from qualtran import drawing 

Register('control', QBit())

@attrs.frozen
class CNOT(Bloq):
    @property
    def signature(self):

        return Signature([
            Register('control', QBit()),
            Register('target', QBit()),
        ])
    

cnot = CNOT()
with open("alg1.svg", "w") as text_file:
    text_file.write(drawing.graphviz.PrettyGraphDrawer(cnot).get_svg().data)



