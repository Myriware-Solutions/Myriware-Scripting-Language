import re
import json

# hashtag I love ChatGPT
def generate_nested_dict_from_string(string, values):
    lines = string.split("\n")
    nested_dict = {}

    for line, value in zip(lines, values):
        line = line.strip()

        if not line:
            continue

        keys = line.strip().split('.')

        current_dict = nested_dict

        for i, key in enumerate(keys):
            if i == len(keys) - 1:
                current_dict[key] = value
            else:
                if key not in current_dict:
                    current_dict[key] = {}
                current_dict = current_dict[key]

    return nested_dict






class Lango:
    def loadConfigFile(langPath: str, schemaPath: str):
        lang_file = open(langPath, 'r')
        lang_data = lang_file.read()
        lang_file.close()
        schema_file = open(schemaPath, 'r')
        schema_data = schema_file.read()
        schema_file.close()
        return Lango.loadConfig(lang_data, schema_data)
    # Main function, taking two strings, the .lang and the schema
    def loadConfig(langIn: str, schemaIn: str) -> dict:
        # print("Hello_world")
        schema_info = re.search(r"{(?P<schema_lang>.*)-(?P<schema_name>.*)}\n(?P<schema_data>[\w\W]*)", schemaIn)
        # print(schema_info)
        schema_data = schema_info.group('schema_data')
        # print(f"Lang Written: {schema_info.group('schema_lang')}\nSchema Name: {schema_info.group('schema_name')}\nData:{schema_data}")
        lang_data = langIn.split("\n")
        # print(lang_data)
        wow = generate_nested_dict_from_string(schema_data, lang_data)
        # print(json.dumps(wow))
        return wow


# DeBug function. Will remove
# Lango.loadConfigFile("./lang/eng.lang", "./lang/_schema.langschema")