from bs4 import BeautifulSoup
from slugify import slugify
import requests
import pathlib
import zipfile
import shutil
import json
import re

# Clean up last run
shutil.rmtree('./entries', ignore_errors=True)

# Sluuurp
r = requests.get('http://privat.bahnhof.se/wb800787/gb/demos/by_id_asc.html')
soup = BeautifulSoup(r.text, 'html5lib')
# print(soup.prettify())
# Header of the table
#  soup.body.center.tbody.contents[1].center.table.tbody.contents[0]

problematicList = []
gameList = []
entries = 0
baseURL = 'http://privat.bahnhof.se/wb800787/gb'

intervalStart = 0
intervalEnd = 400

for r, row in enumerate(soup.body.center.tbody.contents[1].center.table.tbody.contents):
	# TODO: use range
	if (r != intervalStart and r < intervalEnd):
		validEntry = 0

		for c, column in enumerate(row.contents):
			if (c == 0):
				print('ID:', row.contents[c].contents[0])
			elif (c == 1):
				gameTitle = column.a.contents[0]
				gameURL = baseURL + column.a.get('href')[2::]
				print('Title:', gameTitle)
				print('URL:', column.a.get('href'))
				print('Complete URL:', gameURL)

			elif (c == 2):
				developer = column.a.contents[0]
				print('Developer:', developer)
			elif (c == 3):
				platform = column.contents[0]
				print('Platform:', platform)
				if (platform == 'CGB' or platform == 'DMG' or platform == 'DMG,CGB'):
					validEntry = 1
					# use dict and remove this inhumanity
					if (platform == 'DMG,CGB'):
						platform = 'GB'
					if (platform == 'CGB'):
						platform = 'GBC'
					if (platform == 'DMG'):
						platform = 'GB'
			elif (c == 4):
				# print(row.contents[c])
				if (column.contents):
					year = column.contents[0]
					print('Year:', year)
			elif (c == 5):
				if (column.a):
					relativeFileURL = column.a.get('href')[2::]
					# Harcoded for /files/ , use a regex
					fileName = relativeFileURL[7::]
					fileURL = baseURL + column.a.get('href')[2::]
					print('File URL:', column.a.get('href'))
					print('Complete File URL:', fileURL)
			else:
				print(c, column)
		
		if (validEntry):
			# Check for duplicates
			if slugify(gameTitle) in gameList:
				print('Appending developer ')
				gameSlug = slugify(gameTitle) + '-' + slugify(developer[:8])
				if gameSlug in gameList:
					# Really?
					gameSlug = gameSlug + '-1'
					# this is getting pathetic
					if gameSlug in gameList:
						raise ValueError('That\'s pretty bad', gameSlug)
			else:
				gameSlug = slugify(gameTitle)
				

			entries += 1
			romFile = ''
			pathlib.Path('./entries/'+gameSlug).mkdir(parents=True, exist_ok=True)
			gamePage = requests.get(gameURL)
			gameSoup = BeautifulSoup(gamePage.text, 'html5lib')
			screenshotArray = []

			for el in gameSoup.body.table.tbody.contents[2].contents[1].contents:
				# regex this
				screenshotURL = baseURL + el.get('src')[5::]
				screenshotFileName = el.get('src')[14::]
				print(screenshotFileName)
				screenshotArray.append(screenshotFileName)
				screenshotFile = requests.get(screenshotURL)
				if screenshotFile.status_code == 200:
					with open("./entries/"+gameSlug+'/'+screenshotFileName, 'wb') as f:
						f.write(screenshotFile.content)
			
			# Save Release ZIP
			releaseFile = requests.get(fileURL)
			savedReleaseFile = "./entries/"+gameSlug+'/'+fileName
			if releaseFile.status_code == 200:
				with open(savedReleaseFile, 'wb') as f:
					f.write(releaseFile.content)

			
			with zipfile.ZipFile(savedReleaseFile) as myzip:
				for file in myzip.namelist():
						# TODO: for the love of god regex this
						# gb gbc gmb sgb cgb (beware's BGB looks for these)
						if (file[-3:] == 'gbc' or
							 file[-2:] == 'gb' or
							 file[-3:] == 'gmb' or
							 file[-3:] == 'sgb' or
							 file[-3:] == 'cgb' or
							 file[-3:] == 'GMB' or
							 file[-3:] == 'SGB' or
							 file[-3:] == 'CGB' or
							 file[-2:] == 'GB' or
							 file[-3:] == 'GBC'):
							print('Found ROM:', file)
							romFile = file
							myzip.extract(file, "./entries/"+gameSlug+'/')

			if (romFile == ''):
				print('No ROM file found here')
				problematicList.append(gameSlug)

			game = dict( title = gameTitle,
						 	slug = gameSlug, # Slugify
						 	developer = developer,
						 	platform = platform,
						 	typetag = 'demo',
						 	screenshots = screenshotArray, # TODO
						 	rom = romFile,
						 	date = year,
						 	files = [[fileName, 'release']])			

			# Save JSON
			with open("./entries/"+gameSlug+'/game.json', 'w') as f:
				f.write(json.dumps(game, indent=4))

			gameList.append(gameSlug)

			# Save gameList
			with open("./gameList.json", 'w') as f:
				f.write(json.dumps(gameList))

print(problematicList)
print(entries, 'total DMG and GBC entries')