import json
import os
import hashlib
import copy
from difflib import SequenceMatcher

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

pdroms_list = []
for folder in os.listdir('pdroms.de'):
	pdroms_list.append(folder)

print(len(pdroms_list))

with open ('../../gamesList.json') as f:
    game_list = json.load(f)
    print(game_list)

for gameToAdd in pdroms_list:
	for existingGame in game_list:
		simil = similarity(gameToAdd.lower(), existingGame.lower())
		if simil > 0.8:
			print(gameToAdd, existingGame, simil)