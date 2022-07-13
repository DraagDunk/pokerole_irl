import xml.etree.ElementTree as ET
import json
import re

data = 'data.xml'
tree = ET.parse(data)
root = tree.getroot()

dex_entries = [dex for dex in root[3]]

poke_dict = {}
for child in dex_entries[1]:
    poke_dict[child.tag.split('}')[-1]] = child.text

class Pokemon():
    def __init__(self):
        self.a = 1


input_dict = {}
replace_dict = {}

def fill_dict(input_dict, xml_entry):
    for i,child in enumerate(xml_entry):
        # Hack so that child elements with the same tag doesn't overwrite
        # each other.
        replace_dict[child.tag + str(i)] = child.tag
        child.tag += str(i)
        
        
        input_dict[child.tag] = {}
        if list(child) == []:
            input_dict[child.tag] = {child.tag: child.text}
        else:
            fill_dict(input_dict[child.tag], child)

        for i,key in enumerate(child.attrib):
            input_dict[child.tag][key] = child.attrib[key]
    
    return input_dict

input_dict = fill_dict(input_dict, dex_entries[1])

json_string = json.dumps(input_dict, indent = 4)

for key in replace_dict:
    json_string=json_string.replace(key,replace_dict[key])

json_string = re.sub('{.*?}','',json_string)


with open('Bulbasaur.txt','w') as f:
    f.write(json_string)