import xml.etree.ElementTree as ET
import json
import re
import os

data = './data/books.xml'
tree = ET.parse(data)
root = tree.getroot()


def fill_dict(input_dict, replace_dict, xml_entry, trim=True):
    for i, child in enumerate(xml_entry):
        # Hack so that child elements with the same tag doesn't overwrite
        # each other.
        replace_dict[child.tag+str(i)] = child.tag
        child.tag += str(i)

        input_dict[child.tag] = {}
        if list(child) == []:
            input_dict[child.tag] = {child.tag: child.text}
        else:
            fill_dict(input_dict[child.tag], replace_dict, child)

        for i, key in enumerate(child.attrib):
            input_dict[child.tag][key] = child.attrib[key]

    json_string = json.dumps(input_dict, indent=4)

    for key in replace_dict:
        json_string = json_string.replace(key, replace_dict[key])

    if trim:
        json_string = re.sub('{.*?}', '', json_string)
    return json_string


def write_all_files(root):
    os.mkdir('data')
    os.chdir('data')
    cur_dir = os.getcwd()
    for i, entry_type in enumerate(root):
        if i not in [1, 6]: # Hack to avoid Images and MonInstances,
                            # respectively. The former contains strange data
                            # strings and has no good way of being referenced
                            # independently, while the latter is empty.
            entry_type_name = entry_type.tag.split('}')[1]
            os.mkdir(entry_type_name)
            os.chdir(entry_type_name)
            for child in entry_type:
                print(child.tag)
                temp_dict = {}
                replace_dict = {}
                json_string = fill_dict(temp_dict, replace_dict, child)
                name_line = [line.replace(' ', '').replace('"', '') for line in
                             json_string.split('\n') if '"Name": "' in line]
                filename = name_line[0].split(':')[1]+'.txt'
                with open(filename, 'w') as f:
                    f.write(json_string)
            os.chdir(cur_dir)


# Define dicts
input_dict = {}
output_dict = {}

json_string = fill_dict(input_dict, output_dict, root)

with open('./data/output.json', 'w') as f:
    f.write(json_string)
