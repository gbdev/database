# nesworld scraper

## Requirements

Node JS version 7.6 or above. Support for async/await.

## Usage

`npm install` then `npm start`

An entries folder will be created inside the nesworld folder where the results will be put.

The output to the terminal will indicate several things.

- If any error occurs during the scraping.
- If a game/rom does not have a screenshot (will add in the placeholder instead).
- If a game has multiple roms. Manual updating of the game.json will be required.

## Technology
- Node JS
- ES6
- [jsdom](https://www.npmjs.com/package/jsdom)
- [adm-zip](https://www.npmjs.com/package/adm-zip)

## Scripts

Both scripts assume that the files for each `game.json` have been completed and have valid files in the filenames

### scripts/hashes.py

Will loop over ever entry in the `nesworld/entries` folder and generate the 3 hashes for each file, and update the game.json with the result.

This script was modified from `hashes.py` script created by: [Antonio Vivace](https://github.com/avivace)

### scripts/dateModified.py

Will loop over ever entry in the `nesworld/entries` folder and set the date in `game.json` to the last date modified of the file that is marked `default: true`.

## Known issues

Error: `UnhandledPromiseRejectionWarning: Error: EPERM: operation not permitted, mkdir '<filepath>\gbdev\database\scrapers\nesworld\entries'`. Sometimes it has issues accessing the file directory. Try running the app again it usually works the second time. Or create the directory manually.


Created by [Conor Wallace](https://github.com/cwallace3421).


# Scrape: 2018-12-03

## Scraping issues

### Name already on gameList.json (manually removed as they are already in the database)
- back-to-color --> back-to-color-nswld
- bump --> bump-nswld
- dimension-of-miracles --> dimension-of-miracles-nswld
- geometrix --> geometrix-nswld
- it-came-from-planet-zilog --> it-came-from-planet-zilog-nswld
- less-is-more --> less-is-more-nswld
- loop --> loop-nswld
- realtime --> realtime-nswld
- stadin-brankkari --> stadin-brankkari-nswld
- utopia --> utopia-nswld

### No screenshots (placeholder image used instead)
- burly-bear-vs-the-mean-foxes
- cosmica
- egg-racer
- fgb-demo-2-20000817
- fgb-demo-20000321
- gb-fm-synth-20090410
- jetpak-dx-beta-version-001
- jetpak-dx-beta-version-002
- jetpak-dx-beta-version-003
- jetpak-dx-beta-version-004
- jetpak-dx-beta-version-005
- jetpak-dx-beta-version-006
- jetpak-dx-beta-version-007
- little-short-demo-lsd
- little-sound-dj-version-135b-demo
- little-sound-dj-version-319-demo
- mazezam-version-11
- mgb-version-120
- mgb-version-121
- mgb-version-122
- mgb-version-123
- mgb-version-124
- mgb-version-130
- mgb-version-131
- mgb-version-132
- mgb-version-133
- mines
- my-gb-is-your-gb-and-your-gb-is-my-gb
- star-heritage-demo

### Multiple ROMs (main ROM manually selected)
- carillon-editor-version-12
- gameboy-music-compiler-2014-10-21
- gbamatron
- jetpak-dx-beta-version-005
- music-box-version-13
- star-heritage-final
- tochi

### Broken ZIP file (entry deleted manually)
- jetpak-dx-beta-version-007