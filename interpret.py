import os.path
import argparse
import instruct as ins

parser = argparse.ArgumentParser(description='Simple IPPcode18 interpreter')
parser.add_argument('--source', help='File to interpret', required=True)
args = vars(parser.parse_args())

#We got the filename
file = args["source"]

if os.path.isfile(file) is False:
    #TODO: Better error handling
    print("Specified file does not exist, exiting...")
    exit(11)

#Create interpreter object
inter = ins.Interpreter(file)

inter.interpret()
inter.dumpFrames()





