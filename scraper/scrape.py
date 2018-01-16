from bs4 import BeautifulSoup
import requests
import json
import re

r = requests.get('http://privat.bahnhof.se/wb800787/gb/demos/by_id_asc.html')

# Sluuurp
soup = BeautifulSoup(r.text, 'html5lib')

# print(soup.prettify())

# Header of the table
#  soup.body.center.tbody.contents[1].center.table.tbody.contents[0]

entries = 0
baseURL = 'http://privat.bahnhof.se/wb800787/gb'

intervalStart = 0
intervalEnd = 2

for r, row in enumerate(soup.body.center.tbody.contents[1].center.table.tbody.contents):
    # TODO: use range
    if (r != intervalStart and r < intervalEnd):
        validEntry = 0
        print('\nRow', r)

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
            r2 = requests.get(gameURL)
            gameSoup = BeautifulSoup(r2.text, 'html5lib')

            game = dict( title = gameTitle,
                         slug = gameTitle, # Slugify
                         developer = developer,
                         platform = platform,
                         typetag = 'demo',
                         screenshots = '', # TODO
                         rom = '', # TODO
                         date = year,
                         files = [[fileName, 'release']]
                         ) 
            entries+=1
            print(json.dumps(game))
            

print(entries, 'total DMG and GBC entries')