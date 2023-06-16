#output and variable files
f = open("../gen/runtime.json", "w")
f.write('{}')
f.close()
#setup the output file
f = open("../gen/output.json", "w")
f.write('[]')
f.close()

from runline import runline
import tomllib
import os
print("Running Live Interface of Myriware Scripting Language (v0). Anytime, enter 'STOP' to exit.")
while True:
  inpu = input("> ")
  if inpu == "STOP":
    break
  elif inpu == "CONFIG":
    print("Starting CONFIG editor. Enter <key> <true|false>. Enter END to terminate.")
    while True:
      f = open("_config.toml", "r")
      c = f.read()
      data = tomllib.loads(c)
      f.close()
      for par in data:
        print(f"  {par}: {data[par]}")
      config_cmd = input("config> ").split(' ')
      if config_cmd[0] == 'END':
        break
      else:
        if config_cmd[1] == 'true':
          data[config_cmd[0]] = True
        elif config_cmd[1] == 'false':
          data[config_cmd[0]] = False
        else:
          print("Error! Enter 'true' or 'false'!")
      f = open("_config.toml", "w")
      for par in data:
        f.write(f"{par} = {str(data[par]).lower()}\n")
  elif inpu == "FILE":
    file_to_run = input("file> ")
    os.system(f"python3 main.py ../gen/{file_to_run}")
  else:
   runline(inpu)