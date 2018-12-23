import json
import os
import hashlib
import copy

for folder in os.listdir('pdroms.de'):
#for folder in (os.listdir('../entries')[0], ):

	
	path = 'pdroms.de/'+folder+'/'
	print(path)
	with open(path + 'game.json') as f:
		data = json.load(f)

	newData = copy.copy(data)

	if "menu" in newData["title"].lower() or "intro" in newData["title"].lower():
		newData["typetag"] = 'demo'
	else:
		newData["typetag"] = 'game'

	with open(path + 'game.json', 'w') as f:
		f.write(json.dumps(newData,sort_keys=True, indent=4))
		f.close()
