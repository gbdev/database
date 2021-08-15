import os
import json

# elaborate gamesList
gamesList = sorted(os.listdir("../entries"))

# open gamesList file: if it doesn't exist, create it
fd = open("../gamesList.json", "w+")
json.dump(gamesList, fd, sort_keys=True, indent=4)
fd.close()
