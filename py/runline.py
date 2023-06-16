import os
import re
import sys
import json
import traceback
#other files
from runtime import Runtime
from outter import Outter
from tasp import TaspParse
from typer import Typer
#code
def runline(cmd):
  try:
    if (cmd == ""):
      return None
    cmdType = (re.search(r"^\w+(?=[<\s:])", cmd)).group()
    lang_opts = (Runtime.lo()).runline.input
    match cmdType:
    # Match the diffent commands

    # Data-out type commands
      case lang_opts.raw:
        # Prints out the raw value of the input (same as dump, but in json-ish format)
        out = cmd.split(":")[1].strip()
        Outter.out('pri', f"{Typer.parse(out)}")
      case lang_opts.dump:
        # Prints out both the type of input and the value
        out = cmd.split(":")[1].strip()
        Outter.out('pri', f"<{Typer.parse(out)['type']}> {Typer.parse(out)['value']}")
      case lang_opts.echo:
        # Prints out the value of the input
        out = cmd.split(":")[1].strip()
        Outter.out('pri', Typer.parse(out)['value'])
      case lang_opts.vardump:
        # Prints out all the contents of the Runtime
        vars = Runtime.vars().keys()
        for var_name in vars:
          var = Runtime.vars()[var_name]
          Outter.out('pri', f"{var_name}: <{var['type']}> {var['value']}")

    # Variable related commands
      case lang_opts.make:
        # Creates a variable
        varName = re.findall(r"^\w+(?=[<\s]).* (.*):", cmd)[0]
        out = cmd.split(":")
        Runtime.add(varName, Typer.parse(out[1].strip()))
      case lang_opts.remove:
        # Destroys a variable
        out = cmd.split(":")
        Runtime.remove(out[1])

    # MSL based commands
      case lang_opts.execute:
        file_to = Typer.parse(cmd.split(":")[1])['value']
        os.system(f"python3 main.py {file_to}")

    # No command found
      case _:
        Outter.out('err', "Could not find function")
  except Exception as e:
    # stackoverflow.com/questions/1483429/how-do-i-print-an-exception-in-python
    # stackoverflow.com/questions/1278705/when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number
    Outter.out("err", f"  There's an error here\n  Type: {type(e).__name__}\n  File:  {__file__}\n  Line:  {e.__traceback__.tb_lineno}")
    # Use for really, really bad problems
    traceback.print_exc()