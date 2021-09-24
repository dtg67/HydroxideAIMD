class atom:
    def __init__(self, i, ener, type, x, y, z):
        self.i = i
        self.type = type
        self.x = x
        self.y = y
        self.z = z

        def to_dict(self):
            return{
                'i': self.i,
                'type': self.type,
                'x': self.x,
                'y': self.y,
                'z': self.z,
            }

        def __str__(self):
            return (str(self.i) + '\t' +
                    str(self.type) + '\t' +
                    str(self.x) + '\t' +
                    str(self.y) + '\t' +
                    str(self.z) + '\t')

