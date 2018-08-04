# demospotting scraper

This script imports the entire existing database in [Game Boy Demospotting](http://privat.bahnhof.se/wb800787/gb/demos/by_year_desc.html).

Parses metadata and builds a valid `game.json` (complying schema version `draft2`, as defined in this repository) for every GB or GBC entry, then clones every related file, ROM and screenshots, putting them in correct folder structure. Those resources are finally referenced in the `game.json` and the entries are ready to be merged and synced.

## Prerequisites

Python3, pip3, pip, python-slugify

```
apt install python3.6 python2.7
pip install beautifulsoup4
pip install python-slugify
```

## Run

```
python3 scraper.py
```
