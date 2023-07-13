import json
import re
from outter  import Outter
from runtime import Runtime


def is_float(element: any) -> bool:
  # https://stackoverflow.com/questions/736043/checking-if-a-string-can-be-converted-to-float-in-python
  # If you expect None to be passed:
  if element is None:
    return False
  try:
    float(element)
    return True
  except ValueError:
    return False
  
def split_on_commas(string: str) -> list:
  pattern = r',(?![^\[\]]*\])'
  result = re.split(pattern, string)
  return result


class Typer:
  # Main function, string = string that needs parsed, ideally from input
  def parse(string: any) -> any:
    Outter.out('sec', "Parsing unknown: " + string)
    # First, determine what kind of variable you are working with
    variable_type = ''
    string = string.strip()
    # RuntimeVariable
    if (string.find(' ') == -1 and string[0] == '@'):
      var_name = re.findall(r"@([a-zA-Z]*)", string)[0].strip()
      # Indexed Array
      if Runtime.vars()[var_name]["type"] == "Array" and string.find('[') != -1:
        Outter.out("sec", "Finding index of array")
        index = int(re.findall(r"\[([0-9]*)\]", string)[0])
        variable_type = Runtime.vars()[var_name]["value"][index]['type']
        value = Runtime.vars()[var_name]["value"][index]['value']
      # indexed Object
      if Runtime.vars()[var_name]["type"] == "Object" and string.find('[') != -1:
        Outter.out("sec", "Finding index of object")
        index = str(re.findall(r"\[([\w]*)\]", string)[0])
        variable_type = 'any'
        value = Runtime.vars()[var_name]["value"][index]
      else:
        variable_type = Runtime.vars()[var_name]["type"]
        value = Runtime.vars()[var_name]["value"]
    # String
    elif (string[0] == "\"" and string[len(string) - 1] == "\""):
      variable_type = 'String'
      value = re.sub(r"(?<!\\)\"", '', string)
      value = re.sub(r"\\\"", '"', value)
    # String with variables
    elif (string[0] == "`" and string[len(string) - 1] == "`"):
      variable_type = 'String'
      stripped = re.sub(r"(?<!\\)`", '', string)
      placeholders = re.findall(r"(?<!\\){(.*?)}", stripped)
      for placeholder in placeholders:
        var = Typer.parse(placeholder)['value']
        # stripped = re.sub(f"{{{placeholder}}}", var, str(stripped))
        stripped = stripped.replace(f"{{{placeholder}}}", str(var))
      value = stripped
    # Array
    elif (string[0] == "[" and string[len(string) - 1] == "]"):
      variable_type = 'Array'
      strip = string[1:]
      strip = strip[:-1]
      returns = []
      for part in re.split(r"(?<!\\),", strip):
        returns.append(Typer.parse(part))
      value = returns
    elif (string[0] == "{" and string[len(string) - 1] == "}"):
      variable_type = "Object"
      value = json.loads(string)
    # Function
    elif (string[0] == "(" and string[len(string) - 1] == ")"):
      strip = string[1:]
      strip = strip[:-1]
      res = Typer.FunctionParse(strip)
      variable_type = res['type']
      value = res['value']
    # Number
    elif (is_float(string)):
      variable_type = 'Number'
      value = float(string)
    # Error
    else:
      Outter.out('err', "  Error: Did not find this as anything!")
      return None
    Outter.out('sec', "  Found as type: " + variable_type)

    # Return object of type and value
    Outter.out('sec', f"  Returning object of type '{variable_type}' and value '{str(value)}'")
    return {"type": variable_type, "value": value}
  
  # Parses a string that possesses a function
  def FunctionParse(s: str) -> any:
    s = s.strip()
    Outter.out("sec", f"Parsing (functional) input:\n  istr: {s}")
    functionParts = re.search(r"(.*)\((.*)\)", s)
    functTree = functionParts.group(1).split(".")
    functArguments = split_on_commas(functionParts.group(2))
    Outter.out("sec", f"  fmap: {functTree}\n  args: {functArguments}")

    match functTree[0].strip():
    # Packages
      case "File":
        # File, used for opening, reading, editing, etc. files
        match functTree[1]:
          case "load":
            # load(String filename), gets the contents of a file
            file_name = Typer.parse(functArguments[0])
            if file_name['type'] != "String":
              Outter.out("err", f"Expected <String> for filename, got <{file_name['type']}>")
              return None
            load_file = open(file_name['value'], 'r')
            file_content = load_file.read()
            return {"type":"String", "value":file_content}
      case "Json":
        match functTree[1]:
          case "parse":
            stri = Typer.parse(functArguments[0].strip())['value']
            Outter.out("sec", f"Trying to parse:{stri}")
            return {'type':'Object', 'value':json.loads(stri)}

    # Single functions
      case "typeOf":
        # Return the type of input
        fullObj = Typer.parse(functArguments[0].strip())
        Outter.out("sec", f"  fobj: {fullObj}")
        return {"type": "Type", "value": fullObj['type']}
      case "_":
        # DeBug function. Returns the input
        return Typer.parse(functArguments[0].strip())
      case _:
        Outter.out("err", f"Did not find a function or module for '{functArguments}'")
        return None