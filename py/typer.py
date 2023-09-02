import json
import os
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
      # custom class <cClass>
      if Runtime[var_name].type[0] == 'c' and string.find('.') != -1:
        attr = re.search(r'\.([\w]*)', string)
        classes_file = open("./msl/classes.json", 'r')
        pre_ex_dt:dict = json.loads(classes_file.read())
        classes_file.close()
        value = Runtime[var_name].value[attr.group(1)]
        var_t = Runtime[var_name].type[1:]
        variable_type = pre_ex_dt[var_t][attr.group(1)]
      else:
        variable_type = Runtime[var_name].type
        value = Runtime[var_name].value
  # String
    elif ((string[0] == '"' and string[len(string) - 1] == '"') or
          (string[0] == "'" and string[len(string) - 1] == "'")):
      variable_type = 'String'
      value = re.sub(r"(?<!\\)\"", '', string)
      value = re.sub(r"\\\"", '"', value)
      value = value.replace("'", '')
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
    elif (string[0] == "(" and string[len(string) - 1] == ")"):
      strip = string[1:]
      strip = strip[:-1]
      res = _Typer.FunctionParse(strip)
      variable_type = res['type']
      value = res['value']
  # Booleans
    elif (string.lower() == "true" or string.lower() == "t"):
      variable_type = 'Boolean'
      value = True
    elif (string.lower() == "false" or string.lower() == "f"):
      variable_type = 'Boolean'
      value = False
  # Custom User Objects
    elif (string[0] == "*"):
      Outter.out('sec', "Trying to cast custom object")
      parts = re.search(r'\*([\w]*)\(([\w\s"\',.@[\]]*)\)', string)
      classes_file = open("./msl/classes.json", 'r')
      pre_ex_dt:dict = json.loads(classes_file.read())
      classes_file.close()
      if parts.group(1) in pre_ex_dt.keys():
        class_struct:dict = pre_ex_dt[parts.group(1)]
        cls_keys:list = list(class_struct.keys())
        params = parts.group(2).split(',')
        if len(params) is not len(cls_keys):
          Outter.out('err', f'  Incorrect amount of parameters (expected {len(cls_keys)}, got {len(params)})')
          return False
        return_class = { }
        index = 0
        for param in parts.group(2).split(','):
          param = param.strip()
          tipe:Tipe = Tipe(param)
          if tipe.type != class_struct[cls_keys[index]]:
            Outter.out('err', f'  Types mismatch. For {cls_keys[index]}, expected <{class_struct[cls_keys[index]]}>, got <{tipe.type}>')
            return False
          return_class[cls_keys[index]] = tipe.value
          index = index + 1
        variable_type = f'c{parts.group(1)}'
        value = return_class
      else:
        Outter.out('err', f'  Could not find class "{parts.group(1)}"')
        return False
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
          case "load":
            tasp_file = open(Tipe(functArguments[0].strip()).value,"r")
            tasp_tab = Tasp(tasp_file.read())
            tasp_file.close()
            return {'type':'Table','value':tasp_tab}

    # Single functions
      case "typeOf":
        # Return the type of input
        fullObj = Tipe(functArguments[0].strip())
        Outter.out("sec", f"  fobj: {fullObj}")
        return {"type": "Type", "value": fullObj.type}
      case "_":
        # DeBug function. Returns the input
        # return Tipe(functArguments[0].strip())
        var = Tipe(functArguments[0].strip())
        return {"type": var.type, "value": var.value}
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
      parts = re.search(r'(\w*):<([<>()&,=\w\s]*)>([0-9,"\w\s|\/.]*)', string)
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
        "Rows": [ ],
        "AdvSettings": {
          "UsesTaspC": False,
          "TaspCSep": None
        }
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

          case "TaspC":
            Outter.out("sec", "  Using TaspC")
            running_info['AdvSettings']['UsesTaspC'] = True
            if sect_parts.group(2) == "Norm":
              Outter.out('sec', "  Using defualt delimator: |")
              running_info['AdvSettings']['TaspCSep'] = "\n"
            else:
              Outter.out('sec', f"  Using custom delimator: {sect_parts.group(2)}")
              running_info['AdvSettings']['TaspCSep'] = sect_parts.group(2)
      #here
      #put them into rows
      #parts.group(3)
      temp_tab = [ ]
      rows_through = None
      if running_info['AdvSettings']['UsesTaspC'] is True:
        taspC_file = open(Tipe(parts.group(3)).value, 'r')
        taspC = taspC_file.read()
        taspC_file.close()
        rows_through = taspC.split(running_info['AdvSettings']['TaspCSep'])
      else:
        rows_through = parts.group(3).split('|')
      
      for row_info in rows_through:
        temp_row = [ ]
        Outter.out("sec", f"Parsing row: {row_info}")
        for col_info in row_info.split(','):
          Outter.out("sec", f"Adding col: {col_info}")
          temp_row.append(col_info)
        temp_tab.append(temp_row)
      Outter.out("sec", temp_tab)

      # Last
      obj = { }
      if running_info['Ac_Cols'] and running_info['Ac_Rows']:
        Outter.out("sec", "")

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
        for head in running_info['Rows']:
          obj[head] = [ ]
        Outter.out("sec", obj)
        for col in temp_tab:
          Outter.out("sec", f"Adding in info: {col}")
          index = 0
          for row in col:
            Outter.out("sec", f"Adding {row} to {running_info['Rows'][index]}")
            obj[running_info['Rows'][index]].append(Tipe(row))
            index = index + 1

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