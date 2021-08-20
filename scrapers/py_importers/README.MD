# py_importers
Since you can't import top-level packages, a folder named "py_importers" has been created.

In this way, `py_common` module will contain all common files used by various scripts. 

## pouet-scraper

This script imports almost all productions in [Game Boy (and GBC) Pouet Products](https://pouet.net).

It uses bs4 to parse every pouet type of production for every specified platform.

As far as it will be manually tested, it works for GBA too and almost every other platform.

Starting from a Pouet prod's page, it builds a file in compliance with `data model`, generates appropriate json files for
every production, fetches images and updates the global database. 

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