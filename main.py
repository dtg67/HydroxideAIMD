import argparse
import filetopd
from molecule import distances, findwaters, zundel
import pandas as pd
pd.options.mode.chained_assignment = None

#### COMMANDLINE ARGUMENT PASSING ####

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", action = "store",
                    help = "CP2K trajectory file")
parser.add_argument("-L", "--length", action = "store",
                    help = "Simulation box length in angstroms")
parser.add_argument("-N", "--number", action = "store",
                    help = "Number of atoms in simulation")
args = parser.parse_args()
l = float(args.length)
n = int(args.number)
cp2k = args.file


dataframes = filetopd.filetopd(cp2k)
hydroxide = 0

for i in range(max(dataframes['i']) + 1):
    print(i)
    iframes = dataframes.loc[dataframes['i'] == i]
    d = distances(iframes, l, n)
    iframesnamed = findwaters(iframes, d, hydroxide)

    if len(iframesnamed.loc[iframesnamed['mol'] == 'NULL']) > 0:
        iframesnamed = zundel(iframesnamed, d)

    dataframes[dataframes['i'] == i] = iframesnamed
    hydroxide = iframesnamed.loc[iframesnamed['mol'] == 'hydroxide', 'index']

print(len(dataframes[dataframes['mol'] == 'hydroxide']))
dataframes.to_csv('frames.dat', header=True, index=False, sep= ' ')


