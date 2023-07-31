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

        new_files = []

        for file in manifest["files"]:
            if "hash" in file:
                print(
                    f"Removing hashes in file {file['filename']} (entry {manifest['slug']})"
                )
                changes = True
                file.pop("hash")
                new_files.append(file)

        if not mock and changes is True:
            manifest["files"] = new_files
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(manifest, f, indent=4, ensure_ascii=False)
            f.truncate()  # remove remaining part
