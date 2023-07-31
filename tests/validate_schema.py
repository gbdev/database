"""
Validate every game manifest against the JSON schema.
"""

import json
import os

from jsonschema import validate

with open("../game-schema-d4.json") as f:
    schema = json.load(f)

path = "../entries/"
games_list = os.listdir(path)
n = 0

for game in games_list:
    n += 1
    print(f"{n}/{len(games_list)} - Validating {game}..")
    with open(f"../entries/{game}/game.json") as f:
        game = json.load(f)
    validate(game, schema)
