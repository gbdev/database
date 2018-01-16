from bs4 import BeautifulSoup
import requests

r = requests.get('http://privat.bahnhof.se/wb800787/gb/demos/by_id_asc.html')
soup = BeautifulSoup(r.text, 'html5lib')
#print(soup.prettify())

# Header of the table
soup.body.center.tbody.contents[1].center.table.tbody.contents[0]

entries = 0
baseURL = 'http://privat.bahnhof.se/wb800787/gb'

for r, row in enumerate(soup.body.center.tbody.contents[1].center.table.tbody.contents):
    if (r != 0 and r < 400):
        print('\nRow', r)
        for c, column in enumerate(row.contents):
            if (c == 0):
                print('ID:', row.contents[c].contents[0])
            elif (c == 1):
                print('Title:', row.contents[c].a.contents[0])
                print('URL:', row.contents[c].a.get('href'))
                print('Complete URL:', baseURL + row.contents[c].a.get('href')[2::])
            elif (c == 2):
                print('Developer:', row.contents[c].a.contents[0])
            elif (c == 3):
                platform = row.contents[c].contents[0]
                print('Platform:', platform)
                if (platform == 'CGB' or platform == 'DMG' or platform == 'DMG,CGB'):
                    entries+=1
            elif (c == 4):
                #print(row.contents[c])
                if (row.contents[c].contents):
                    print('Year:', row.contents[c].contents[0])
            elif (c == 5):
                if (row.contents[c].a):
                    print('File URL:', row.contents[c].a.get('href'))
                    print('Complete File URL:', baseURL + row.contents[c].a.get('href')[2::])
            else:
                print(c, column)

print(entries, 'total DMG and GBC entries')
