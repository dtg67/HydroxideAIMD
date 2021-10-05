class atom:
    def __init__(self, i, type, x, y, z, residue, index, mol):
        self.i = i
        self.type = type
        self.x = x
        self.y = y
        self.z = z
        self.residue = residue
        self.index = index
        self.mol = mol

    def to_dict(self):
        return {
            'i': self.i,
            'type': self.type,
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'residue': self.residue,
            'index': self.index,
            'mol': self.mol
        }

    def __str__(self):
        return (str(self.i) + '\t' +
                str(self.type) + '\t' +
                str(self.x) + '\t' +
                str(self.y) + '\t' +
                str(self.z) + '\t' +
                str(self.residue) + '\t' +
                str(self.index) + '\t' +
                str(self.mol))

    def to_gauss(self):
        return (str(self.type) + '\t' +
                str(self.x) + '\t' +
                str(self.y) + '\t' +
                str(self.z) + '\t')