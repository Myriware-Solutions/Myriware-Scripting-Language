import re
import sys
import json
from runline import runline
from outter import Outter

def RunFile(fileToRun: str):
    #needed functions
    #get the name of the file that will parsed
    fileContents = open(fileToRun).read()
    #out(fileContents)
    #remove all comments, and whitespace
    fileContents = re.sub(r"^#.*$", "", fileContents, 0, re.MULTILINE)
    fileContents = re.sub(r"^%[\w\W]*%$", "", fileContents, 0, re.MULTILINE)
    fileContents = re.sub(r"\n", "", fileContents, 0, re.MULTILINE)
    #out(fileContents)
    #now, process each string as a command
    commandLines = fileContents.split(";")
    #out(commandLines)
    index = 1
    for cmd in commandLines:
        res = runline(cmd)
        if not res:
            Outter.out('err', f'Something is wrong on line {index}\n    {cmd}')
        index = index + 1