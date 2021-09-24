import argparse
import filetopd
from molecule import distances

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

distanceframe = dataframes.loc[dataframes['i'] == 0]
distanceframe = distanceframe[['x','y','z']]

mindist, index = distances(distanceframe, l, n)

