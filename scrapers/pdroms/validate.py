import os
from pathlib import Path
import re
import json
from jsonschema import validate

with open ('../../game-schema-d3.json') as f:
    gameSchema = json.load(f)

for folder in os.listdir(Path('pdroms.de')):
    path = 'pdroms.de/'+folder
    print(path)
    with open (path+'/game.json') as f:
        game = json.load(f)
    print(validate(game, gameSchema))

