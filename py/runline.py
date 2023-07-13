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
from imports import Imports
from conn import ExternalConnections
#code
def runline(cmd):
  try:
    if (cmd == ""):
      return None
    cmdType = (re.search(r"^\w+(?=[<\s:])", cmd)).group()
    cmdData = (re.search(r".*?:(.*)", cmd)).group(1)
    lang_opts = (Runtime.lo()).runline.input
    match cmdType:
    # Match the diffent commands

    # Data-out type commands
      case lang_opts.raw:
        # Prints out the raw value of the input (same as dump, but in json-ish format)
        Outter.out('pri', f"{Typer.parse(cmdData)}")
      case lang_opts.dump:
        # Prints out both the type of input and the value
        Outter.out('pri', f"<{Typer.parse(cmdData)['type']}> {Typer.parse(cmdData)['value']}")
      case lang_opts.echo:
        # Prints out the value of the input
        Outter.out('pri', Typer.parse(cmdData)['value'])
      case lang_opts.vardump:
        # Prints out all the contents of the Runtime
        vars = Runtime.vars().keys()
        for var_name in vars:
          var = Runtime.vars()[var_name]
          Outter.out('pri', f"{var_name}: <{var['type']}> {var['value']}")

    # Variable related commands
      case lang_opts.make:
        # Creates a variable
        varName = re.findall(r"^\w+(?=[<\s]).* (\w*):", cmd)[0]
        Runtime.add(varName, Typer.parse(cmdData))
      case lang_opts.remove:
        # Destroys a variable
        Runtime.remove(cmdData)

    # MSL based commands
      case lang_opts.execute:
        # Run a MSL file
        file_to = Typer.parse(cmd.split(":")[1])['value']
        os.system(f"python msl.zip file {file_to}")
      case lang_opts.imports_name:
        # Import manager
        import_cmd = re.findall(r"^\w+(?=[<\s]).* (\w*):", cmd)[0]
        match import_cmd:
          case "get":
            # Get an module/lang
            Imports.get(Typer.parse(cmdData)['value'])

    # External Connection based commands
      case lang_opts.conn_name:
        sub = re.search(r"(.*):", cmd).group(1).split(' ')
        print("Extern (loading...)")
        match sub[1]:
          case "udp":
            match sub[2]:
              case lang_opts.conn.udp.send:
                print("doing stuff")
                cmd_info = re.search(r".*:([0-9.]+) ([0-9]+) (.*)$", cmd)
                ExternalConnections.UDP.send(cmd_info.group(1), int(cmd_info.group(2)), Typer.parse(cmd_info.group(3))["value"])
              case lang_opts.conn.udp.wait:
                print("doing stuff too")
                cmd_info = re.search(r".*:([0-9.]+) ([0-9]+)", cmd)
                ExternalConnections.UDP.wait(cmd_info.group(1), int(cmd_info.group(2)))

    # Other language type functions (static names)
      case "for":
        # SYNTAX    for <#_num_|[_array_]|$_function_>::<cmd>
        args = re.search(r"for (.*)::(.*)$", cmd)
        match args.group(1)[0]:
          case "#":
            # The hashtag will do the following command x times (the number proceeding the #). Also, it will replace the $FOR_INT with it's current number
            for x in range(0, int(args.group(1)[1:])):
              runline(args.group(2).replace("$FOR_INT", str(x)))


    # No command found
      case _:
        Outter.out('err', "Could not find function")
  except Exception as e:
    # stackoverflow.com/questions/1483429/how-do-i-print-an-exception-in-python
    # stackoverflow.com/questions/1278705/when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number
    Outter.out("err", f"  There's an error here\n  Type: {type(e).__name__}\n  File:  {__file__}\n  Line:  {e.__traceback__.tb_lineno}")
    # Use for really, really bad problems
    traceback.print_exc()