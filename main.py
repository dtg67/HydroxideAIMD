import argparse
import filetopd
from molecule import distances, findwaters, zundel
import pandas as pd
from analysis import hydroxide_o_to_water_h, coordination_num, hydroxide_o_to_water_h_frames, cn2gaussian
import numpy as np
pd.options.mode.chained_assignment = None

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", action="store",
                    help="CP2K trajectory file")
parser.add_argument("-L", "--length", action="store",
                    help="Simulation box length in angstroms")
parser.add_argument("-N", "--number", action="store",
                    help="Number of atoms in simulation")
args = parser.parse_args()
length = float(args.length)
n = int(args.number)
cp2k = args.file

dataframes = filetopd.filetopd(cp2k)
hydroxide = 0
num_frames = max(dataframes['i']) + 1
num_water_h = (n - 2) // 3 * 2
o_to_h_mat = np.zeros( (int(num_frames), int(num_water_h)) )
cn = []

for i in range(num_frames):
    print(i)
    iframes = dataframes.loc[dataframes['i'] == i]
    d = distances(iframes, length, n)
    iframesnamed = findwaters(iframes, d, hydroxide)

    if len(iframesnamed.loc[iframesnamed['mol'] == 'NULL']) > 0:
        iframesnamed = zundel(iframesnamed, d)

    hydroxide = iframesnamed.loc[iframesnamed['mol'] == 'hydroxide', 'index']
    dataframes[dataframes['i'] == i] = iframesnamed
    ho_o_w_h_iframes = hydroxide_o_to_water_h_frames(iframes)
    ho_o_w_o_iframes = hydroxide_o_to_water_o_frames(iframes)
    o_to_h_array = hydroxide_o_to_water_h(ho_o_w_h_iframes, length)
    o_to_o_array = hydroxide_o_to_water_o(ho_o_w_o_iframes, length)
    cn.append(coordination_num(ho_o_w_h_iframes, 2.5, o_to_h_array))
    lastcn = cn[-1]
    o_to_h_mat[i, ] = np.sort(o_to_h_array[1:])
    o_to_h_mat[i, ] = np.sort(o_to_h_array[1:])
    cn2gaussian( lastcn, iframesnamed, i)


dataframes.to_csv('frames.dat', header=True, index=False, sep=' ')
# np.savetxt('cn.dat', np.array(cn), fmt='%1i')
b = np.matrix(o_to_h_mat)
np.savetxt('HO_O_to_W_H_dist.dat', b, fmt='%.4f')

