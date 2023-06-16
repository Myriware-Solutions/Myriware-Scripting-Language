#output and variable files
f = open("../gen/runtime.json", "w")
f.write('{}')
f.close()
#setup the output file
f = open("../gen/output.json", "w")
f.write('[]')
f.close()

from runline import runline
from runtime import Runtime
import tomllib
import os
print(Runtime.l()['console']['output']['opening'])
while True:
  inpu = input("> ")
  if inpu == Runtime.l()['console']['input']['stop']:
    break
  elif inpu == Runtime.l()['console']['config']['mainInput']:
    print(Runtime.l()['console']['config']['opening'])
    while True:
      f = open("_config.toml", "r")
      c = f.read()
      data = tomllib.loads(c)
      f.close()
      for par in data:
        print(f"  {par}: {data[par]}")
      config_cmd = input(">> ").split(' ')
      if config_cmd[0] == Runtime.l()['console']['config']['stop']:
        break
      else:
        if config_cmd[1] == 'true':
          data[config_cmd[0]] = True
        elif config_cmd[1] == 'false':
          data[config_cmd[0]] = False
        else:
          data[config_cmd[0]] = f"\"{config_cmd[1]}\""
      f = open("_config.toml", "w")
      for par in data:
        f.write(f"{par} = {str(data[par]).lower()}\n")
  elif inpu == Runtime.l()['console']['file']:
    file_to_run = input(">> ")
    os.system(f"python3 main.py ../gen/{file_to_run}")
  else:
   runline(inpu)