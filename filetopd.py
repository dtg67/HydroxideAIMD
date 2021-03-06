import pandas as pd
import re
import atom

def filetopd(cp2kfile):
    i = -1
    dataframes = []
    frame = atom.atom(type = "NULL", x = 0, y = 0, z = 0, i = i, residue="NULL", index = 0, mol = "NULL")
    with open(cp2kfile) as file_in:
        for line in file_in:
            if re.search(r"VMD", line):
                i += 1
                index = 0
            elif  re.search(r"( |H|O )", line):
                lines = re.split(r'\s+', line)
                frame.i = i
                frame.type = lines[1]
                frame.x = float(lines[2])
                frame.y = float(lines[3])
                frame.z = float(lines[4])
                frame.index = index
                frame.residue = "NULL"
                frame.mol = "NULL"
                appendframe = atom.atom(frame.i, frame.type, frame.x,
                                        frame.y, frame.z,  frame.residue, frame.index, frame.mol)
                dataframes.append(appendframe.to_dict())
                index += 1

    return pd.DataFrame.from_records(dataframes)