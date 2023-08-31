import json
import re
import traceback
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

  def __str__(self):
    if self.type == "Array":
      returnable = [ ]
      for item in self.value:
        #returnable.append(f"<{item.type}> {item.value}")
        returnable.append(item.value)
      return str(returnable)
    else:
      #return f"<{self.type}> {self.value}"
      return str(self.value)


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
  # TableSpeak Object
    elif (string[0] == "="):
      variable_type = "Table"
      value = Tasp(string)
  # Function
#TODO: fix this mess
    elif (string[0] == "(" and string[len(string) - 1] == ")"):
      strip = string[1:]
      strip = strip[:-1]
      res = _Typer.FunctionParse(strip)
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
            stri = Tipe(functArguments[0].strip()).value
            Outter.out("sec", f"Trying to parse:{stri}")
            return {'type':'Object', 'value':json.loads(stri)}
      case "Tasp":
        match functTree[1]:
          case "getCol":
            table = Tipe(functArguments[0].strip()).value
            col = table.getColumn(Tipe(functArguments[1].strip()).value)
            return {'type':'Array','value':col}

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

### TASP ###

# Example:
#   <
#     (Active=Columns), 
#     (Columns=Name & Age & Gender)
#   >
#   "Anthony", 16, "Male" |
#   "Billy", 15, "Male" |
#   "Katty", 15, "Female"
# ;
# =Example:<(Active=Columns), (Columns=Name & Age & Gender)>"Anthony", 16, "Male" |"Billy", 15, "Male" |"Katty", 15, "Female";

class Tasp:
  def __init__(self, toParse:str) -> None:
    placeholder = _TableSpeak.parse(toParse)
    self.table = placeholder['data']
    self.meta = placeholder['meta']
    self.name = placeholder['name']

  def makeReadable(self):
    statement = f"Reading {self.name} (meta name)"
    running_info = self.meta
    if running_info['Ac_Cols'] and running_info['Ac_Rows']:
      Outter.out("sec", "WIP")
    elif running_info['Ac_Cols']:
      for column in self.meta['Cols']:
        statement = f"{statement}\n{column}"
        for row in self.table[column]:
          statement = f"{statement}\n  {row}"
    elif running_info['Ac_Rows']:
      Outter.out("sec", "WIP")
    return statement
  
  def getColumn(self, colName:str):
    running_info = self.meta
    if running_info['Ac_Cols'] and not running_info['Ac_Rows']:
      return self.table[colName]
    else:
      Outter.out("err", "Wrong type of Table Object! (Contains rows)")
    

class _TableSpeak:
  def parse(inputString:str) -> dict:
    string = inputString.replace(" ",'').replace("\n",'')
    Outter.out("sec", f"Parsing {string}")
    parts = [ ]
    try:
      parts = re.search(r'(\w*):<([<>()&,=\w\s]*)>([0-9,"\w\s|]*)', string)
      parts_info = f"""
Table Name   : {parts.group(1)}
Table Header : {parts.group(2)}
Table Info   : {parts.group(3)}
    """
      Outter.out("sec", parts_info)
      running_info = {
        "Ac_Cols": False,
        "Ac_Rows": False,
        "Cols": [ ],
        "Rows": [ ]
      }
      for header_sect in parts.group(2).split(","):
        Outter.out("sec", f"Header Sect: {header_sect}")
        sect_parts = re.search(r"\(([\w]*)=([\w&\s]*)\)", header_sect)
        match sect_parts.group(1):
          case "Active":
            Outter.out("sec", "  Checking Actives")
            if sect_parts.group(2) == "Columns&Rows" or sect_parts.group(2) == "Rows&Columns":
              running_info["Ac_Cols"] = True
              running_info["Ac_Rows"] = True
              Outter.out("sec", "  Both")
            elif sect_parts.group(2) == "Columns":
              running_info["Ac_Cols"] = True
              Outter.out("sec", "  Cols")
            elif sect_parts.group(2) == "Rows":
              running_info["Ac_Rows"] = True
              Outter.out("sec", "  Rows")
              
          case "Columns":
            Outter.out("sec", "  Setting Columns")
            cols = sect_parts.group(2).split('&')
            Outter.out("sec", cols)
            running_info["Cols"] = cols

          case "Rows":
            Outter.out("sec", "  Setting Rows")
            rows = sect_parts.group(2).split('&')
            Outter.out("sec", rows)
            running_info["Rows"] = rows
      #here
      #put them into rows
      #parts.group(3)
      temp_tab = [ ]
      for row_info in parts.group(3).split('|'):
        temp_row = [ ]
        Outter.out("sec", f"Parsing row: {row_info}")
        for col_info in row_info.split(','):
          Outter.out("sec", f"Adding col: {col_info}")
#TODO: Add Tipe parse
          temp_row.append(col_info)
        temp_tab.append(temp_row)
      Outter.out("sec", temp_tab)

      # Last
      obj = { }
      if running_info['Ac_Cols'] and running_info['Ac_Rows']:
        Outter.out("sec", )

      elif running_info['Ac_Cols']:
        for head in running_info['Cols']:
          obj[head] = [ ]
        Outter.out("sec", obj)
        for row in temp_tab:
          Outter.out("sec", f"Adding in info: {row}")
          index = 0
          for col in row:
            Outter.out("sec", f"Adding {col} to {running_info['Cols'][index]}")
            obj[running_info['Cols'][index]].append(Tipe(col))
            index = index + 1
#TO

      elif running_info['Ac_Rows']:
        Outter.out("sec", )

      else:
        Outter.out("sec", )

      Outter.out("sec", obj)
      return {
        "data":obj,
        "meta":running_info,
        "name":parts.group(1)
      }
    
    except Exception as e:
      Outter.out("sec", "Failed")
      Outter.out("err", f"  There's an error here\n  Type: {type(e).__name__}\n  File:  {__file__}\n  Line:  {e.__traceback__.tb_lineno}")
      traceback.print_exc()
      return False