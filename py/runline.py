import inspect
import json
import os
import random
import re
import traceback
import importlib.util
import tomllib
#other files
from outter import Outter
from typer import Tipe
from typer import Tasp
from imports import Imports
from conn import ExternalConnections
from lango import lo
from lango import loadConfig
from _runtime import Runtime
from z_tips import Tips
#langpack
Lang = lo()
#print("Loaded LangPack:", Lang)
def dict_to_toml(d):
    toml_lines = []
    for key, value in d.items():
        if isinstance(value, str):
            toml_lines.append(f'{key} = "{value}"')
        elif isinstance(value, int):
            toml_lines.append(f'{key} = {value}')
        elif isinstance(value, bool):
            toml_lines.append(f'{key} = {str(value).lower()}')
    toml_string = "\n".join(toml_lines)
    return toml_string.lower()
#code
def runline(cmd):
  try:
    if (cmd == ""):
      return None
    cmdType = (re.search(r"^[\w*]+(?=[<\s:])", cmd)).group()
    cmdData = (re.search(r".*?:(.*)", cmd)).group(1)
    match cmdType:
    # Match the diffent commands

    # Data-out type commands
      case Lang.runline.input.raw:
        # Prints out the raw value of the input (same as dump, but in json-ish format)
        Outter.out('pri', f"{Tipe(cmdData)}")
      case Lang.runline.input.dump:
        # Prints out both the type of input and the value
        val = Tipe(cmdData)
        Outter.out('pri', f"<{val.type}> {val.value}")
      case Lang.runline.input.echo:
        # Prints out the value of the input
        Outter.out('pri', Tipe(cmdData))
      case Lang.runline.input.vardump:
        # Prints out all the contents of the Runtime
        vars = Runtime.keys()
        for var_name in vars:
          var = Runtime[var_name]
          Outter.out('pri', f"{var_name}: <{var.type}> {var.value}")

    # Variable related commands
      case Lang.runline.input.make:
        # Creates a variable
        varName = re.findall(r"^\w+(?=[<\s]).* (\w*):", cmd)[0]
        ##Runtime.add(varName, Typer.parse(cmdData))
        Runtime[varName] = Tipe(cmdData)
      case Lang.runline.input.remove:
        # Destroys a variable
        varName = re.findall(r"^\w+(?=[<\s]).* (\w*):", cmd)[0]
        del Runtime[varName]
      case "defclass":
        # Create a caste for a custom class
        class_name = re.findall(r"^\w+(?=[<\s]).* (\w*):", cmd)[0]
        class_attr_strs = cmdData.replace(' ','').split(',')
        temp = { }
        for class_attr in class_attr_strs:
          parts = re.search(r'([\w]*)=([\w]*)', class_attr)
          temp[parts.group(1)] = parts.group(2)
        #add it to classes file
        classes_file = open("./msl/classes.json", 'r')
        pre_ex_dt = json.loads(classes_file.read())
        pre_ex_dt[class_name] = temp
        classes_file.close()
        classes_file = open("./msl/classes.json", 'w')
        classes_file.write(json.dumps(pre_ex_dt))
        classes_file.close()

    # MSL based commands
      case "config":
        arg_stri = cmdData.replace(' ',''); args = arg_stri.split(',')
        key_name = Tipe(args[0]).value; key_value = Tipe(args[1]).value
        pre_config = loadConfig()
        pre_config[key_name] = key_value
        config_f = open("msl/config.toml", 'w')
        config_f.write(dict_to_toml(pre_config))
        config_f.close()
      case Lang.runline.input.execute:
        # Run a MSL file
        file_to = Tipe(cmd.split(":")[1]).value
        os.system(f"python msl.zip file {file_to}")
      case Lang.runline.input.imports_name:
        # Import manager
        import_cmd = re.findall(r"^\w+(?=[<\s]).* (\w*):", cmd)[0]
        match import_cmd:
          case "get":
            # Get an module/lang
            Imports.get(Tipe(cmdData).value)
      case Lang.runline.input.make_input_data:
        # Add a user input
        varName = re.findall(r"^\w+(?=[<\s]).* (\w*):", cmd)[0]
        Runtime[varName] = Tipe(input(f"{varName}> "))
      case "*":
        # Run a Modules function
        ps = re.search(r"\* ([a-zA-z]*) ([a-zA-z]*):(.*)", cmd)
        module_name  = ps.group(1)
        module_path  = f"./msl/imports/{module_name}.py"

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        test_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_module)

        function_name = ps.group(2)

        # Check if the function exists in the module
        if hasattr(test_module, function_name) and callable(getattr(test_module, function_name)):
            # Get the function using getattr and call it
            func = getattr(test_module, function_name)
            # Get the function's signature
            signature = inspect.signature(func)

            # Count the number of parameters
            num_parameters = len(signature.parameters)
            if num_parameters == 0:
              func()
            elif num_parameters == 1:
              function_paramas = Tipe(ps.group(3)).value
              func(function_paramas)
        else:
            print(f"The function '{function_name}' does not exist or is not callable.")

    # External Connection based commands
      case Lang.runline.input.conn_name:
        sub = re.search(r"(.*):", cmd).group(1).split(' ')
        print("Extern (loading...)")
        match sub[1]:
          case "tcp":
            match sub[2]:
              case Lang.runline.input.conn.tcp.send:
                print("doing stuff")
                cmd_info = re.search(r".*:([0-9.]+) ([0-9]+) (.*)$", cmd)
                ExternalConnections.TCP.send(cmd_info.group(1), int(cmd_info.group(2)), Tipe(cmd_info.group(3)).value)
              case Lang.runline.input.conn.tcp.wait:
                print("doing stuff too")
                cmd_info = re.search(r".*:([0-9.]+) ([0-9]+)", cmd)
                ExternalConnections.TCP.wait(cmd_info.group(1), int(cmd_info.group(2)))
      case "Chatter":
        port_ip = re.search(r"([0-9.a-z]+) ([0-9]+)", cmdData)
        ExternalConnections.ChitChat.startChitChat(port_ip.group(1), int(port_ip.group(2)))


    # Other language type functions (static names)
      case "for":
        # SYNTAX    for <#_num_|[_array_]|$_function_>::<cmd>
        args = re.search(r"for (.*)::(.*)$", cmd)
        match args.group(1)[0]:
          case "#":
            # The hashtag will do the following command x times (the number proceeding the #). Also, it will replace the $FOR_INT with it's current number
            for x in range(0, int(args.group(1)[1:])):
              runline(args.group(2).replace("$FOR_INT", str(x)))
          case "@":
            # This refferances a variable
            var = Tipe(args.group(1))
            match var.type:
              case "Array":
                # replaces the $FOR_VAL with the value of theat index
                for item in var.value:
                  runline(args.group(2).replace("$FOR_VAL", item.value))

    # humorous
      case "tipme":
        random_index = random.randint(0, len(Tips) - 1)
        random_tip = Tips[random_index]
        print("    " + random_tip)

    # variable representation
      case "mkreadable":
        table = Tipe(cmdData).value
        asStr = table.makeReadable()
        Outter.out("pri", asStr)


    # No command found
      case _:
        Outter.out('err', "Could not find function")
  except Exception as e:
    # stackoverflow.com/questions/1483429/how-do-i-print-an-exception-in-python
    # stackoverflow.com/questions/1278705/when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number
    # Outter.out("err", f"  There's an error here\n  Type: {type(e).__name__}\n  File:  {__file__}\n  Line:  {e.__traceback__.tb_lineno}")
    # Use for really, really bad problems
    traceback.print_exc()
    Outter.out('err', "Error processing input.")
    return False
  return True