"""
Checks if every file mentioned in every game manifest exists on the file system.
This script should be run after having verified that the game manifest validates again the JSON schema.
"""

import json
import os
import progressbar


path = "../entries/"
games_list = os.listdir(path)

for game in progressbar.progressbar(games_list, redirect_stdout=True):
    with open(f"../entries/{game}/game.json") as f:
        game = json.load(f)
    # print(f"Checking {game['slug']}..")
    base_dir = f"{path}/{game['slug']}"

    for file in game["files"]:
        full_path = os.path.join(base_dir, file["filename"])
        if not os.path.isfile(full_path):
            raise Exception(
                f'{file["filename"]} found in manifest but not on disk (entry {game["slug"]})'
            )

    for screenshot in game["screenshots"]:
        full_path = os.path.join(base_dir, screenshot)
        if not os.path.isfile(full_path):
            raise Exception(
                f'{screenshot} found in manifest but not on disk (entry {game["slug"]})'
            )

    # print(
    #    f"{game['slug']}: {len(game['files'])} file(s), {len(game['screenshots'])} screenshot(s)"
    # )
