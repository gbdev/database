"""
Validate every game manifest against the JSON schema.
"""

import json
import os
import progressbar

from jsonschema import validate

with open("../game-schema-d4.json") as f:
    schema = json.load(f)

path = "../entries/"
games_list = os.listdir(path)
n = 0


for game in progressbar.progressbar(games_list, redirect_stdout=True):
    n += 1
    print(f"Validating {game}..")
    with open(f"../entries/{game}/game.json") as f:
        game = json.load(f)
    validate(game, schema)
