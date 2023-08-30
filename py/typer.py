import json
import re
from outter  import Outter
from _runtime import Runtime


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

class Tipe:
  def __init__(self, value:any) -> None:
    base = _Typer.parse(value)
    self.value = base['f_value']
    self.type  = base['f_type']


class _Typer:
  # Main function, string = string that needs parsed, ideally from input
  def parse(string:str) -> dict:
    Outter.out('sec', "Parsing unknown: " + string)
    # First, determine what kind of variable you are working with
    variable_type = ''
    string = string.strip()
  # RuntimeVariable
    if (string.find(' ') == -1 and string[0] == '@'):
      var_name = re.findall(r"@([a-zA-Z]*)", string)[0].strip()
      # Indexed Array
      if Runtime[var_name].type == "Array" and string.find('[') != -1:
        Outter.out("sec", "Finding index of array")
        index = int(re.findall(r"\[([0-9]*)\]", string)[0])
        variable_type = Runtime[var_name].value[index].type
        value = Runtime[var_name].value[index].value
      # indexed Object
      if Runtime[var_name].type == "Object" and string.find('[') != -1:
        Outter.out("sec", "Finding index of object")
        index = str(re.findall(r"\[([\w]*)\]", string)[0])
#TODO: find the type?
        variable_type = 'any'
        value = Runtime[var_name].value[index]
      else:
        variable_type = Runtime[var_name].type
        value = Runtime[var_name].value
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
        var = Tipe(placeholder).value
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
        returns.append(Tipe(part))
      value = returns
    elif (string[0] == "{" and string[len(string) - 1] == "}"):
      variable_type = "Object"
      value = json.loads(string)
  # Function
#TODO: fix this mess
    elif (string[0] == "(" and string[len(string) - 1] == ")"):
      strip = string[1:]
      strip = strip[:-1]
      res = _Typer.FunctionParse(strip)
      variable_type = res.type
      value = res.value
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

    # Changing from unassigned dict to Type object
    # return {"type": variable_type, "value": value}
    return {"f_type": variable_type, "f_value": value}


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
            file_name = Tipe(functArguments[0])
            if file_name.type != "String":
              Outter.out("err", f"Expected <String> for filename, got <{file_name.type}>")
              return None
            load_file = open(file_name.value, 'r')
            file_content = load_file.read()
            return {"type":"String", "value":file_content}
      case "Json":
        match functTree[1]:
          case "parse":
            stri = Tipe(functArguments[0].strip())['value']
            Outter.out("sec", f"Trying to parse:{stri}")
            return {'type':'Object', 'value':json.loads(stri)}

    # Single functions
      case "typeOf":
        # Return the type of input
        fullObj = Tipe(functArguments[0].strip())
        Outter.out("sec", f"  fobj: {fullObj}")
        return {"type": "Type", "value": fullObj.type}
      case "_":
        # DeBug function. Returns the input
        return Tipe(functArguments[0].strip())
      case _:
        Outter.out("err", f"Did not find a function or module for '{functArguments}'")
        return None