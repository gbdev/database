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
