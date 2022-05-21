"""
This scripts tries to fix entries with non-url safe slugs, changing the slug inside the manifest and renaming the folders.

Actions:

- Replaces `.` with `-` if the `.` was in a "v1.0" like string
- Removes the character `.`
- Removes the character `&`
- Removes the character `!`

Each of these can happen once per entry.

Notes:

Run from the scripts folder

Always re run every test after applying such actions.

The full output of this script should be included in the message of the commit applying these changes the as the results can be quite distructive.
"""

import json
import os
import re

entries_list = os.listdir("../entries")

n = 0
possible_duplicates = []

mock = True

for entry in entries_list:
    if (
        "." in entry
        or "&" in entry
        or "!" in entry
        or "(" in entry
        or ")" in entry
        or "'" in entry
    ):
        n = n + 1
        with open(f"../entries/{entry}/game.json", "r+") as f:
            data = json.load(f)
            if "." in entry:
                x = re.search(r"v\d+\.\d", data["slug"])
                if x:
                    # if the slug had a "vN.M" string, replace . with a -
                    new_slug = data["slug"].replace(".", "-")
                else:
                    # otherwise, just remove the dot
                    new_slug = data["slug"].replace(".", "")
            if "&" in entry:
                # Remove the &
                new_slug = data["slug"].replace("&", "")
            if "!" in entry:
                # Remove the !
                new_slug = data["slug"].replace("!", "")
            if "(" in entry or ")" in entry:
                new_slug = data["slug"].replace("(", "").replace(")", "")
            if "'" in entry:
                new_slug = data["slug"].replace("'", "")
            # Make everything lowercase
            new_slug = new_slug.lower()

            if os.path.isdir(f"../entries/{new_slug}"):
                # Shouldn't happen more than once
                #  if it does, handle this manually
                new_slug = new_slug + "-1"
                print(f"Target slug exists, changing to {new_slug}")
                possible_duplicates.append(new_slug)

            print(f"Setting new slug: {data['slug']} -> {new_slug}")
            data["slug"] = new_slug  # <--- add `id` value.
            if not mock:
                f.seek(0)  # <--- should reset file position to the beginning.
                json.dump(data, f, indent=4)
                f.truncate()  # remove remaining part
        print(f"Renaming: ../entries/{entry} -> ../entries/{new_slug}")
        if not mock:
            os.rename(f"../entries/{entry}", f"../entries/{new_slug}")

print(f"{n} total entries changed")
print(f"Possible duplicates: {possible_duplicates} ")
