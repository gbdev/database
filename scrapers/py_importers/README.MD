# py_importers
Since you can't import top-level packages, a folder named "py_importers" has been created.

In this way, `py_common` module will contain all common files used by various scripts. 

## pouet-scraper

This script imports almost all productions in [Game Boy (and GBC) Pouet Products](https://pouet.net).

It uses bs4 to parse every pouet type of production for every specified platform.

As far as it will be manually tested, it works for GBA too and almost every other platform.

Starting from a Pouet prod's page, it builds a file in compliance with `data model`, generates appropriate json files for
every production, fetches images and updates the global database. 

## gambit-importer
As usual, run the script, everything will be in beta folder.

## yaronet-thread
This is a special m******* script. It works if and only if a certain zip file has been provided.

This has been made in this way, because scraping everything would have taken too many hours.

Additionally, websites like gamejolt and itch.io are un-scrapable, resulting in swears and other awful things.

Technically, they are scrapable, but just with selenium... which it's boring and it will take ages to me to implement it.

Two lists are present, gb-autom-source (which barely automatize some entries), and gb-manual-source that contains path added manually.

This cost me something like 2 hours.

If you're reading this, and you are a dev, and you've uploaded your productions on itch.io or any other
website that doesn't provide a direct link here is a tip for you: ALWAYS UPLOAD YOUR PRODS SOMEWHERE, WHERE
IT IS POSSIBLE TO HAVE A DIRECT LINK.

Thanks, have a nice day.

Instruction: download the zip file and place it in scrapers/py_importers/py_common/tmp
The script will do the rest!

As usual, everything will be in beta folder 

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