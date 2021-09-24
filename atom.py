import pandas as pd

class atom:
    def __init__(self, i, type, x, y, z):
        self.i = i
        self.type = type
        self.x = x
        self.y = y
        self.z = z

    def to_dict(self):
        return {
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

#
# def filetopd(cp2kfile):
#     i = 0
#     dataframes = []
#     frame = atom.atom(type = "NULL", x = 0, y = 0, z = 0, i = i)
#     with open(cp2kfile) as file_in:
#         for line in file_in:
#             if re.search(r"VMD", line):
#                 i += 1
#             elif  re.search(r"( |H|O )", line):
#                 lines = re.split(r'\s+', line)
#                 # lines = line.split('\t')[0]
#                 # lines = lines.split("\t")
#                 print(lines)
#                 frame.i = i
#                 frame.type = lines[1]
#                 frame.x = float(lines[2])
#                 frame.y = float(lines[3])
#                 frame.z = float(lines[4])
#                 appendframe = atom.atom(frame.i, frame.type, frame.x, frame.y, frame.z)
#                 dataframes.append(appendframe)
#                 print(appendframe)
#
#     return pd.DataFrame.from_records([dict2frame.to_dict() for dict2frame in dataframes])