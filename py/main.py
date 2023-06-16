import re
import sys
import json
#output and variable files
f = open("../gen/runtime.json", "w")
f.write('{}')
f.close()
#setup the output file
f = open("../gen/output.json", "w")
f.write('[]')
f.close()
#other files
from parvar import *
from runline import runline
#make the runtime variables and needed arrays, objs, etc
fileContents = ""
output = [ ]
#needed functions
def out(s):
  if (type(s) is str):
    print("[New Section]\n" + s + "\n")
  elif ((type(s) is list) or (type(s) is object)):
    print("[New Section]\n" + json.dumps(s) + "\n")
#get the name of the file that will parsed
fileToRun = sys.argv[1]
fileContents = open(fileToRun).read()
#out(fileContents)
#remove all comments, and whitespace
fileContents = re.sub(r"^#.*$", "", fileContents, 0, re.MULTILINE)
fileContents = re.sub(r"\n", "", fileContents, 0, re.MULTILINE)
#out(fileContents)
#now, process each string as a command
commandLines = fileContents.split(";")
#out(commandLines)
for cmd in commandLines:
  runline(cmd)