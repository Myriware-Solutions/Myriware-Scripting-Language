from runline import runline
from runtime import Runtime
import tomllib
import os

def RunConsole():
  #output and variable files
  f = open("./msl/gen/runtime.json", "w")
  f.write('{}')
  f.close()
  #setup the output file
  f = open("./msl/gen/output.json", "w")
  f.write('[]')
  f.close()

  print(Runtime.l()['console']['output']['opening'])
  while True:
    inpu = input("> ")
    if inpu == Runtime.l()['console']['input']['stop']:
      break
    else:
      runline(inpu)