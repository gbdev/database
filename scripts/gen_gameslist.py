import os
import json

entries_list = os.listdir('../entries')

# Serializing json 
json_object = json.dumps(entries_list, indent = 4)
  
# Writing to sample.json
with open("sample.json", "w") as outfile:
    outfile.write(json_object)
