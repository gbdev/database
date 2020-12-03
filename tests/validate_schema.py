from jsonschema import validate
import json

with open("../game-schema-d3.json") as f:
    schema = json.load(f)

with open("../gamesList.json") as f:
    games_list = json.load(f)

for game in games_list:
    print(f"Validating {game}..")
    with open(f"../entries/{game}/game.json") as f:
        game = json.load(f)
    validate(game, schema)
