# py_importers
Since you can't import top-level packages, a folder named "py_importers" has been created.

In this way, `py_common` module will contain all common files used by various scripts. 

## pouet-scraper

This script imports almost all productions in [Game Boy (and GBC) Pouet Products](https://pouet.net).

It uses bs4 to parse every pouet type of production for every specified platform.

As far as it will be manually tested, it works for GBA too and almost every other platform.

Starting from a Pouet prod's page, it builds a file in compliance with `data model`, generates appropriate json files for
every production, fetches images and updates the global database. 

## gambit-scraper

gambit-prods page is a mess.

Not only you will need to scrape everything, but once scraped, roms will be
in a strange pdb format.

gambit-prods provide a link where to download all those roms in a normal gb/gbc format in a single zip file.

This script will download that zip file and it will move every gb file into an appropriate folder, with screenshots
and game.json

### Prerequisites
All the libraries are in `requirements.txt` (in theory), just use pip to install them. 
```
pip install -r requirements.txt
```

### Run
```
python3 <script>.py
```

#### Tested with Python 3.9.6