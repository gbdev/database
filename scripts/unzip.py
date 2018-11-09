import zipfile
import os
from pathlib import Path
import json
import re
import copy


p = re.compile('(.*\.c*gbc*|\.dmg)', re.IGNORECASE)

for folder in os.listdir(Path('pdroms.de')):
	path = 'pdroms.de/'+folder
	print(path)
	with open (path+'/game.json') as f:
		gameData = json.load(f)

	newData = copy.copy(gameData)

	if gameData["rom"][-3:] == 'zip':
		with zipfile.ZipFile(path + '/' + gameData["rom"]) as zip_ref:
			zip_ref.extractall(path)
		
		for el in os.listdir(path):
			m = p.match(el)
			if (m != None):
				print(m.group())
				newRom = m.group()
				newData.pop('rom', None)
		
		newData["rom"] = newRom
		newData["files"] = [ gameData["rom"] ]


		if (newData["rom"][-3:].lower() == 'gbc' or newData["rom"][-3:].lower() == 'cgb'):
			newData["platform"] = 'GBC'
		else:
			newData["platform"] = 'GB'

		with open(path + '/game.json', 'w') as f:
			json.dump(newData, f)

