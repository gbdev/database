import json
import os
import hashlib
import sys

DEFAULT_ENTRIES_FOLDER = "../entries"
DEFAULT_BETA_FOLDER = "../scrapers/py_importers/py_common/beta/"


def get_file_hash(filename, alg, chunksize=131072):
    if alg == "sha256":
        h = hashlib.sha256()
    elif alg == "sha1":
        h = hashlib.sha1()
    elif alg == "md5":
        h = hashlib.md5()

    with open(filename, "rb", buffering=0) as f:
        for b in iter(lambda: f.read(chunksize), b""):
            h.update(b)
    return h.hexdigest()


"""
In JSON we have multiple files for each rom. This could lead sometimes to not have any executable file in that list.
For each file in "files" field in JSON, take the extension.
If that file is a homebrew, returns its path, otherwise, if files specified in the list of files in the JSON does not contain any executable gb file, return -1.
"""


def look_for_rom(files):
    for f in range(0, len(files)):
        ext = files[f]["filename"].split(".")[-1]
        if ext.lower() in ["gb", "gbc", "cgb", "gba", "agb", "sgb"]:
            return files[f]["filename"]

    return -1


"""
   given a path of a folder containing rom to be added in the database
   it says if we're adding duplicates or nope

    you should run this after you've developed a new script (there shoulnd't be duplicates in the entries folder) 

    Since you need to check if entries in beta folder are in the main folder, you will first need to run this function
    by passing entries folder then beta folder.

    params: beta flag --> if on, it won't print again the recap at the end and it will print a special [BETA] tag if a rom turns
    out to be duplicated
"""
d = dict()


def check_entries_folder(entries_path, beta=False):
    # check if entries path doesnt end with /
    if entries_path[-1] != "/":
        entries_path += "/"

    for folder in os.listdir(entries_path):
        with open(entries_path + folder + "/game.json") as f:
            data = json.load(f)

        game_path = entries_path + folder + "/"

        rom_name = look_for_rom(data["files"])

        """
        If rom has been found, get its hash (we cannot assume it is already saved in the json, because it could be missing)
        """
        if rom_name != -1:
            try:
                hash = get_file_hash(game_path + rom_name, "md5")

                """
                If hash is not in d, let's add the hash as a key and a list of a value.
                We will then append the slug to the list, with slug rom's hash as a key.
                """
                if hash not in d:
                    d[hash] = {"filename": rom_name, "appears_in": []}

                d[hash]["appears_in"].append(data["slug"])

                if beta:
                    # print(rom_name + " " + hash)
                    if len(d[hash]["appears_in"]) > 1:
                        print(
                            "[BETA] "
                            + f"{d[hash]['filename']} found in entries: {d[hash]['appears_in']}"
                        )

            except:
                print(data["slug"] + ": hash can't be retrieved.")
        else:
            print(data["slug"] + ": hash can't be retrieved.")

        with open("rom-hashes.json", "w") as json_file:
            json.dump(d, json_file, indent=4)

    """
    If a list contains more than one slug, it means that those slugs are the same,
    because we've met twice or more times the same rom: every time we've encountered a rom we have stored its hash,
    then having two or more values means that we've the same rom saved in multiple directories (it has more than one slug,
    but it is the same rom).
    """
    if not beta:
        for key in d:
            if len(d[key]["appears_in"]) > 1:
                print(f"{d[key]['filename']} found in entries: {d[key]['appears_in']}")
                # print("hash: " + key)


def main():
    args = sys.argv[1:]

    if "-h" in args or "--help" in args:
        print(
            "Usage: ./dupe_finder <entries folder>\n\t<entries_folder> are roms to be checked, hardcoded in source at DEFAULT_ENTRIES_FOLDER = "
            + DEFAULT_ENTRIES_FOLDER
            + "\n"
            + "Parameters:\n\t--beta <entries beta folder>:\n\t\tabsolute path where the beta folder is: new entries that are going to be merged\n"
            + "\t\thardcoded in source at DEFAULT_BETA_FOLDER = "
            + DEFAULT_BETA_FOLDER
            + "\n"
            + "\t--help\n"
            + "\t\tshow this message"
        )
        exit(0)

    check_entries_folder(DEFAULT_ENTRIES_FOLDER)

    if len(args) > 0 and args[0].lower() == "--beta":
        print("\n" + "Duplicated Beta Entries:")
        check_entries_folder(DEFAULT_BETA_FOLDER, True)


main()
