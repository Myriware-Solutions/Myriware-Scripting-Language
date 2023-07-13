import os
import sys
from console import RunConsole
from runfile import RunFile

print("msl...")
print(sys.argv)
try:
  match sys.argv[1]:
    case "console":
      RunConsole()
    case "file":
      RunFile(sys.argv[2])
    case _:
      print("...msl needs more information <console|file PATH>")
except IndexError:
  print("...msl needs more information <console|file PATH>")