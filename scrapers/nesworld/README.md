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


Created by [Conor Wallace](https://github.com/cwallace3421).


# Scrape: 2018-12-03

## Issues

### No screenshots (placeholder image used instead)
- bump
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
- loop
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
- stadin-brankkari
- star-heritage-demo
- utopia

### Multiple ROMs (main ROM manually selected)
- carillon-editor-version-12
- gameboy-music-compiler-2014-10-21
- gbamatron
- jetpak-dx-beta-version-005
- music-box-version-13
- stadin-brankkari
- star-heritage-final
- tochi

### .cgb ROM format (platform set to GBC)
- brikster
- columnsdx
- ironhike
- maniacminer

### Broken ZIP file (entry deleted manually)
- jetpak-dx-beta-version-007