"""
Checks if every file mentioned in every game manifest exists on the file system.
This script should be run after having verified that the game manifest validates again the JSON schema.
"""

import json
import os

path = "../entries/"
games_list = os.listdir(path)

for game in games_list:

    with open(f"../entries/{game}/game.json") as f:
        game = json.load(f)
    print(f"Checking {game['slug']}..")
    for file in game["files"]:
        if file["filename"] not in os.listdir(f"{path}/{game['slug']}"):
            raise Exception(f'{file["filename"]} found in manifest but not on disk (entry {game["slug"]})')
    for screenshot in game["screenshots"]:
        if screenshot not in os.listdir(f"{path}/{game['slug']}"):
            raise Exception(f'{screenshot} found in manifest but not on disk (entry {game["slug"]})')
    print(f"{game['slug']}: {len(game['files'])} file(s), {len(game['screenshots'])} screenshot(s)")
