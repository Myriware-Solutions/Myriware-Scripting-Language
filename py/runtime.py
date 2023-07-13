import json
import tomllib
from lango import Lango
class Runtime:


  def loadConfig():
    f = open("./msl/config.toml", "r")
    c = f.read()
    data = tomllib.loads(c)
    f.close()
    return data
  

  def l():
    f = open("./msl/config.toml", "r")
    c = f.read()
    data = tomllib.loads(c)
    f.close()
    return Lango.loadConfigFile(f"./msl/lang/{data['lang']}.lang", "./msl/lang/_msl.sch")
  

  def lo():
    class DictToObject:
      def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(self, key, DictToObject(value))
            else:
                setattr(self, key, value)
    return DictToObject(Runtime.l())
  

  def vars():
    # return the variables stored in the runtime file
    f = open('./msl/gen/runtime.json')
    variables = json.loads(f.read())
    f.close()
    return variables
  

  def add(name, data):
    #add data to the variable file
    f = open("./msl/gen/runtime.json", "r")
    pre = json.loads(f.read())
    f.close()
    pre[name] = data
    f = open("./msl/gen/runtime.json", "w")
    f.write(json.dumps(pre))
    f.close()


  def remove(key):
    # Remove key/value from the runtime
    f = open("./msl/gen/runtime.json", "r")
    pre = json.loads(f.read())
    f.close()
    del pre[key.strip()]
    f = open("./msl/gen/runtime.json", "w")
    f.write(json.dumps(pre))
    f.close()


  def out(data):
    #add data to the output file
    f = open("./msl/gen/output.json", "r")
    pre = json.loads(f.read())
    f.close()
    pre.append(data)
    f = open("./msl/gen/output.json", "w")
    f.write(json.dumps(pre))
    f.close()