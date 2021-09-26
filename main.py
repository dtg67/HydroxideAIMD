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


for i in range(max(dataframes['i']) + 1):

    iframes = dataframes.loc[dataframes['i'] == i]
    d = distances(iframes, l, n)
    iframesnamed = findwaters(iframes, d)
    print(iframesnamed.loc[iframes['mol'] == 'hydroxide'])
    if "NULL" in iframesnamed['mol']:
        iframesnamed = zundel(iframesnamed, d)

    dataframes[dataframes['i'] == i] = iframesnamed


print(len(dataframes[dataframes['mol'] == 'hydroxide']))
dataframes.to_csv('frames.dat', header=True, index=False, sep= ' ')


