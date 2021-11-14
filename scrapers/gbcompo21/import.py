import csv, os
from slugify import slugify
from strsimpy.levenshtein import Levenshtein
import json
from shutil import copyfile

levenshtein = Levenshtein()

#  Friday 1 October 2021 02:00:00 to unix datestamp epoch
date = 1633053600

os.mkdir("exported")

# From the first round of ranking of the gbcompo21
# titles must match validation.csv title
shortlist = [
    "<corrib75>",
    "Core Machina",
    "Dango Dash",
    "Dawn Will Come",
    "El Dueloroso",
    "Fix My Heart",
    "GB Corp.",
    "GBCspelunky",
    "Glory Hunters",
    "Marla and the Elemental Rings DEMO",
    "Porklike GB",
    "Rebound",
    "Renegade Rush",
    "Sushi Nights",
    "Shock Lobster",
    "Unearthed",
    "Rhythm Land",
    #
    #
    "Zilogized",
    "HELLO WORLD",
]

shortlisted = 0
with open("gbcompo21.csv", newline="") as csvfile:
    spamreader = csv.DictReader(csvfile)
    for row in spamreader:
        with open("validation.csv", newline="") as csvfile:
            validation = csv.DictReader(csvfile)
            for validated in validation:
                if validated["submission_url"] == row["submission_url"]:
                    validated_values = validated
        if validated_values["Qualifies?"] == "TRUE":
            problematic = False
            typetag = validated_values["Category"].lower()
            if typetag == "tool":
                typetag = "homebrew"
            gameObj = {
                "title": row["title"],
                "slug": slugify(row["title"]),
                "developer": row["user"],
                "typetag": typetag,
                "tags": ["gbcompo21"],
                "website": row["game_url"],
                "date": date,
                "screenshots": [],
                "files": [],
            }
            if validated_values["Open Source"] == "TRUE":
                gameObj["repository"] = validated_values["Open Source repository"]
                gameObj["tags"].append("Open Source")
                gameObj["license"] = validated_values["OS License"]

            if validated_values["title"] in shortlist:
                gameObj["tags"].append("gbcompo21-shortlist")
                shortlisted += 1
            else:
                continue

            # Find the folder in the gbcompo21 repository
            d = 1000000
            for directory in os.listdir("gbcompo21/entries"):
                d2 = levenshtein.distance(directory, row["title"])
                if d2 < d:
                    d = d2
                    matched = directory
            # print(f"{row['title']} || {matched} || {d} || ")

            if d > 2:
                problematic = True

            # Create a directory:

            ex_gamedir = f'exported/{slugify(row["title"])}'
            os.mkdir(ex_gamedir)

            if not problematic:
                gamedir = f"gbcompo21/entries/{matched}"
                files = os.listdir(gamedir)

                for file in files:
                    # Look for GB and GBC roms
                    if file[-3:].lower() == "gbc" or file[-3:].lower() == ".gb":
                        copyfile(f"{gamedir}/{file}", f"{ex_gamedir}/{file}")
                        fileobj = {"playable": "true", "filename": file}
                        gameObj["files"].append(fileobj)
                    # Look for screenshots (pics and GIFs)
                    if (
                        file[-3:].lower() == "png"
                        or file[-3:].lower() == "jpg"
                        or file[-3:].lower() == "gif"
                        or file[-3:].lower() == "bmp"
                    ):
                        copyfile(f"{gamedir}/{file}", f"{ex_gamedir}/{file}")
                        gameObj["screenshots"].append(file)

            if len(gameObj["files"]) == 0:
                print("No ROM files found", row["title"])
            with open(f"{ex_gamedir}/game.json", "w") as fp:
                js = json.dumps(gameObj, indent=4)
                fp.write(js)

        # if not problematic:

        # Find GB or GBC files

        # Find screenshots

        # print(gameObj)

# Check if every shortlisted entry was found
if len(shortlist) != shortlisted:
    print("Some shortlist tag has not been applied")
