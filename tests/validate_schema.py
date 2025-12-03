"""
Validate every game manifest against the JSON schema.
"""

import json
import os
import progressbar
import sys

from jsonschema import validate, ValidationError

with open("../schemas/game-schema-d5.json") as f:
    schema = json.load(f)

path = "../entries/"
games_list = os.listdir(path)
n = 0
errors = 0

for game in progressbar.progressbar(games_list, redirect_stdout=True):
    n += 1
    try:
        with open(f"../entries/{game}/game.json") as f:
            game_metadata = json.load(f)
    
        validate(game_metadata, schema)
    except Exception as e:
        errors += 1
        print(f"Failed {game}: \n {e}")
        # sys.exit(1)

if errors > 0:
    print(f"\n {errors} entrie(s) have failed validation")
    sys.exit(1)