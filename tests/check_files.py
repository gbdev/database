import json
import os

path = "../entries/"
games_list = os.listdir(path)

for game in games_list:
    with open(f"../entries/{game}/game.json") as f:
        game = json.load(f)
    for file in game["files"]:
        if file["filename"] not in os.listdir(f"{path}/{game['slug']}"):
            raise Exception(f'error {file["filename"]} found in manifest but not on disk')
