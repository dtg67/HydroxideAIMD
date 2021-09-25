import argparse
import filetopd
from molecule import distances, findwaters
import pandas as pd
from scipy.stats import gaussian_kde

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
    iframes = findwaters(iframes, d)
    print(iframes.loc[iframes['mol'] == 'hydroxide'])
    iframes.to_csv('frames.txt', sep='\t', index=False, header=True)



