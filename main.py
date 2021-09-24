import argparse


#### COMMANDLINE ARGUMENT PASSING ####

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", action = "store",
                    help = "CP2K trajectory file")
parser.add_argument("-L", "--length", action = "store",
                    help = "Simulation box length in angstroms")
parser.add_argument("-N", )
args = parser.parse_args()
l = float(args.length)
cp2k = args.file

