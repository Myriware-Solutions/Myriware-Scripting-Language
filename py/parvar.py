import re
import json
from runtime import *
#this class is used for parsing variables of different kinds
class parvar:
  #most things will pass through here, to see if it's a variable
  def var(v):
    if (v.find("@") != -1):
      val = Runtime.vars()[v.replace('@','').strip()]
      print("  Using "+str(val)+" for var-reference "+v)
      return val
    else:
      return v
  def array(s):
    print("Processing array...")
    arrayString = (re.search(r"\[.*\]", s)).group();
    match = re.search(r"\[(.*?)(?<!\\)],?", arrayString)
    if match:
        items = match.group(1).split(",")
        returns = [ ]
        for item in items:
          returns.append((parvar.var(str(item))).strip())
        return returns
    else:
      return None