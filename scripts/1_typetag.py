"""
Change entries with "homebrew" as typetag to "tool"
"""

import json
import os

entries_list = os.listdir("../entries")
mock = False

for entry in entries_list:
    with open(f"../entries/{entry}/game.json", "r+") as f:
        changes = False
        manifest = json.load(f)
        
        if "typetag" in manifest:
            if manifest["typetag"] == "homebrew":
                manifest["typetag"] = "tool"
                print(manifest["slug"], "HOMEBREW -> TOOL")
                changes = True
        else:
            print(manifest["slug"], "No typetag")
        print(manifest)
        if not mock and changes is True:
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(manifest, f, indent=4, ensure_ascii=False)
            f.truncate()  # remove remaining part
