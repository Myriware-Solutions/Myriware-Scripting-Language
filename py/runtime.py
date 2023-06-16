import json
class Runtime:
  def vars():
    f = open('../gen/runtime.json')
    variables = json.loads(f.read())
    f.close()
    return variables
  def add(name, data):
    #add data to the variable file
    f = open("../gen/runtime.json", "r")
    pre = json.loads(f.read())
    f.close()
    pre[name] = data
    f = open("../gen/runtime.json", "w")
    f.write(json.dumps(pre))
    f.close()
  def remove(key):
    # Remove key/value from the runtime
    f = open("../gen/runtime.json", "r")
    pre = json.loads(f.read())
    f.close()
    del pre[key.strip()]
    f = open("../gen/runtime.json", "w")
    f.write(json.dumps(pre))
    f.close()
  def out(data):
    #add data to the output file
    f = open("../gen/output.json", "r")
    pre = json.loads(f.read())
    f.close()
    pre.append(data)
    f = open("../gen/output.json", "w")
    f.write(json.dumps(pre))
    f.close()