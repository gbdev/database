"""
Validate every game manifest against the JSON schema.
"""

from jsonschema import validate
import json
import os, sys

with open("../game-schema-d4.json") as f:
    schema = json.load(f)

path = "../entries/"
games_list = os.listdir(path)

for game in games_list:
    print(f"Validating {game}..")
    with open(f"../entries/{game}/game.json") as f:
        game = json.load(f)
    validate(game, schema)
