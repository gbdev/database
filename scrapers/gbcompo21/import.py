import csv, os
from slugify import slugify
from strsimpy.jaro_winkler import JaroWinkler

jarowinkler = JaroWinkler()

#  Friday 1 October 2021 02:00:00 to unix datestamp epoch
date = 1633053600

with open("gbcompo21.csv", newline="") as csvfile:
    spamreader = csv.DictReader(csvfile)
    for row in spamreader:
        gameObj = {
            "title": row["title"],
            "slug": slugify(row["title"]),
            "developer": row["user"],
            "typetag": "game",
            "tags": ["gbcompo21"],
            "website": row["game_url"],
            "date": date,
        }
        if len(row["Open Source repository"]) > 1:
            gameObj["repository"] = row["Open Source repository"]
            gameObj["tags"].append("Open Source")
        # if row["title"] in shortlist:
        # 	gameObj["tags"].append("gbcompo21-top20")

        d = 1000000
        for directory in os.listdir("gbcompo21/entries"):
            d2 = jarowinkler.distance(directory, row["title"])
            if d2 < d:
                d = d2
                matched = directory
        print(gameObj["title"])
        print(f"{row['title']} || {matched} || {d} || ")

        # print(gameObj)
