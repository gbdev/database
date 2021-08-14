# pouet-scraper

This script imports almost all productions in [Game Boy (and GBC) Pouet Products](https://pouet.net).

It uses bs4 to parse every pouet type of production for every specified platform.

As far as it will be manually tested, it works for GBA too and almost every other platform.

Starting from a Pouet prod's page, it builds a file in compliance with `data model`, generates appropriate json files for
every production, fetches images and updates the global database. 

## Prerequisites
All the libraries are in `requirements.txt` (in theory), just use pip to install they. 
```
pip install -r requirements.txt
```

## Run
```
python3 pouet.py
```

#### Tested with Python 3.9.6