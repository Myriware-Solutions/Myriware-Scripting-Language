import re
import sys
import json
from runline import runline

def RunFile(fileToRun: str):
    #output and variable files
    f = open("./runtime.json", "w")
    f.write('{}')
    f.close()
    #setup the output file
    f = open("./output.json", "w")
    f.write('[]')
    f.close()
    #other files
    #make the runtime variables and needed arrays, objs, etc
    fileContents = ""
    output = [ ]
    #needed functions
    #get the name of the file that will parsed
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