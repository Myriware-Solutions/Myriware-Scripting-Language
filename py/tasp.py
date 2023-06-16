import json
import re
def RowCol(mpo):
  cols = [ ]
  match mpo['args'][0]:
    case 'u':
#print('      Unquoted')
      # split on space
      cols = re.split(' ', mpo['data'])
#print('       ',cols)
    case 'q':
#print('      Quoted')
      # find all \"(.*?)(?<!\\)\"
      cols = re.findall(r"\"(.*?)(?<!\\)\"", mpo['data'])
  return cols
def arrayClean(array):
  return_array = []
  for part in array:
    if (part != '' and part != '\n' and part != None and part != ' '):
      return_array.append(part.strip())
  return return_array
def TaspParse(s):
  # create the return object
  return_obj = { }
  # begin processing
#print("preparing tasp...\n" + s)
  s = re.sub(r"#.*$", "", s, 0, re.MULTILINE) # remove one-line comments
  s = re.sub(r"\/\*[\s\S]*?\*\/", "", s, 0, re.MULTILINE) # remove multi-line comments
  s = re.sub(r"\n", "", s, 0, re.MULTILINE) # remove return line
  s = re.sub(r" +", ' ', s, 0) # remove long spaces
#print("\nun-commented contents\n" + s)
  # make groups of different objects using: r"@(.*):([\s\S]*?)end"
  # use to find a list of groups: r"@.*:[\s\S]*?end"
  object_matches = re.findall(r"@[\s\S]*?end", s)
#print("\nmatches:\n" + json.dumps(object_matches))
  for match in object_matches:
    match_stats = re.search(r"@(.*?):([\s\S]*?)end", match)
    object_name = match_stats.groups()[0].strip();
    object_info = {
      "rows": False,
      "cols": False,
    }
#print("processing object " + object_name)
    return_obj[object_name] = {}
    object_members = re.split(r"(?<!\\);", match_stats.groups()[1])
    for member in object_members:
      if (member == '' or member == '\n' or member == ' '):
        continue
      mp = re.search(r"(?P<type>.*)<(?P<args>.*)>:(?P<data>.*)", member).groups()
      #print("  Found this:", mp)
      mpo = {
        'type': mp[0].strip(),
        'args': mp[1].strip(),
        'data': mp[2].strip()
      }
#print("  processing in-line info:\n    type:"+mpo['type']+"\n    args:"+mpo['args']+"\n    data:"+mpo['data'])
      match mpo['type']:
        case 'Columns':
#print('      Processing Column')
          object_info['cols'] = True
          cols = RowCol(mpo)
          for col in cols:
            return_obj[object_name][col] = None
        case 'Rows':
#print('      Processing Row')
          rows = RowCol(mpo)
          object_info['rows'] = True
          if (object_info['cols']):
#print('        Using 3-Dim')
            for col in return_obj[object_name]:
              for row in rows:
                return_obj[object_name][col][row] = None
          else:
            for row in rows:
              return_obj[object_name][row] = None
        case 'Data':
#print('      Processing Data')
          if (object_info['rows'] and object_info['cols']):
#print('      Adding 3-Dim data')
            msg="TODO"
          elif (object_info['rows']):
#print('      Adding Rows')
            for index, row in enumerate(re.split(',', mpo['data']), start=0):
              return_obj[object_name][list(return_obj[object_name].keys())[index]] = arrayClean(re.split(' ', row))
          # process the columns types
          elif (object_info['cols']):
            for name in list(return_obj[object_name].keys()):
              return_obj[object_name][name] = []
#print('      Adding Columns')
            # loop through each row of data
            for row_index, row in enumerate(re.split(r"(?<!\\),", mpo['data']), start=0):
              to_clean = None
              if (mpo['args'][0] == 'u'):
                to_clean =  re.split(' ', row)
              else:
                to_clean = re.findall(r"\"(.*?)(?<!\\)\"", row)
#print("        Row data:" ,to_clean)
              cols = arrayClean(to_clean)
              col_names = list(return_obj[object_name].keys())
#print("        Columns names:", col_names)
              for col_index, col in enumerate(cols, start=0):
#print('        '+object_name+' '+str(col_index)+' '+col)
                return_obj[object_name][col_names[col_index]].append(re.sub(r"\\", '', col))
          else:
#print('error')
            return None
#print("Returning TASP Results")
  return(return_obj)