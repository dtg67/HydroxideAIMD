import argparse
import filetopd
from molecule import distances
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

file = open("distance.dat", "a")
for i in range(max(dataframes['i']) + 1):

    iframes = dataframes.loc[dataframes['i'] == i]

    distanceframe = iframes[['x','y','z']]
    #
    mindist, index, d = distances(distanceframe, l, n)
    frame0 = iframes.loc[iframes['index'] == index[0]]
    frame1 = iframes.loc[iframes['index'] == index[1]]
    frame0 = pd.concat([frame0, frame1])
    frameO = frame0.loc[frame0['type'] == 'O']
    #
    frameH = iframes.loc[iframes['type'] == 'H']
    frameall = pd.concat([frameO, frameH])
    frameall = frameall[['x', 'y', 'z']]
    #
    mindist, index1, d = distances(frameall, l, 130)
    d = sorted(d[1:])
    file.write(str(d).strip('[]').replace(',', '\t') + '\n')



