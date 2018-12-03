const AdmZip = require('adm-zip');
const fs = require('fs');
const http = require('http');
const log = require('./log');
const path = require('path');

const url = 'http://www.nesworld.com/';
const base = path.resolve(__dirname, 'entries');

/**
 * Push game meta and downloaded contents to the file system asynchronously (kind of).
 * @param {Object[]} meta - An array of game meta objects.
 * @returns {Promise} Promise that will resolve when all game meta is processed and complete.
 */
exports.push = (meta) => {
    if (fs.existsSync(base)) rimraf(base);
    fs.mkdirSync(base);

    log.title('Creating directories and downloading assets based on Meta');

    const promises = [];
    for (let i = 0; i < meta.length; i++) {
        promises.push(handleGameMeta(meta[i]));
    }
    return Promise.all(promises);
}

/**
 * Given game meta, download screenshots, download rom zip, and build folder structure for game.
 * @async
 * @param {Object} game - The game meta.
 */
async function handleGameMeta(game) {
    const gamePath = path.resolve(base, game.slug);
    fs.mkdirSync(gamePath);

    // Download Screenshots
    if (game.screenshots.length === 1 && game.screenshots[0] === 'placeholder.png') {
        fs.copyFileSync(path.resolve(__dirname, 'placeholder.png'), path.resolve(gamePath, 'placeholder.png'));
    } else {
        for (let i = 0; i < game.screenshots.length; i++) {
            const screenshotFilename = cleanPath(game.screenshots[i]);
            await download(url + game.screenshots[i], path.resolve(gamePath, screenshotFilename));
            game.screenshots[i] = screenshotFilename;
        }
    }

    // Download ROM zip and extract
    const romZipFilename = cleanPath(game.rom);
    await download(url + game.rom, path.resolve(gamePath, romZipFilename));
    const romName = unzip(game.slug, path.resolve(gamePath, romZipFilename));

    game.rom = romName ? romName : '??????';

    fs.writeFileSync(path.resolve(gamePath, 'game.json'), JSON.stringify(game, null, 4));
}

/**
 * Unzip a zip file to a directory with the slug name, keep only rom files, delete the rest of the contents.
 * @param {string} slug - The slug of the game name.
 * @param {string} zipFilePath - The file path for the zip file.
 * @returns {string} The potential main rom file name.
 */
function unzip(slug, zipFilePath) {
    let stage = 'Loading ZIP: ' + zipFilePath;
    try {
        const slugFilePath = path.resolve(base, slug);
        const zip = new AdmZip(zipFilePath);

        // Get possible ROM files
        stage = 'Getting possible ROMs in ZIP file: ' + zipFilePath;
        const possibleRoms = zip.getEntries().map(e => e.entryName).filter(e => /\.c?gbc?$/g.test(e.toLowerCase()));
        if (possibleRoms.length > 1) {
            log.warn(`Multiple possible ROMs found for '${slug}' (game.json will need updated): Count ${possibleRoms.length}`);
        } else if (possibleRoms.length === 0) {
            throw new Error('No possible ROMs found');
        }

        // Extract Zip
        const extractedFilePath = path.resolve(slugFilePath, 'zip');
        stage = 'Extracting all contents of ZIP to: ' + extractedFilePath;
        zip.extractAllTo(extractedFilePath);

        // Move ROMs to Root
        for (let i = 0; i < possibleRoms.length; i++) {
            const oldFilePath = path.normalize(path.resolve(extractedFilePath, possibleRoms[i]));
            const newFilePath = path.normalize(path.resolve(slugFilePath, cleanName(cleanPath(possibleRoms[i]))));
            stage = 'Moving ROM from \"' + oldFilePath + '\" to \"' + newFilePath;
            fs.renameSync(oldFilePath, newFilePath);
        }

        // Delete Zip and other extracted contents
        stage = 'Deleting ZIP file: ' + zipFilePath;
        fs.unlinkSync(zipFilePath);
        stage = 'Deleting extracted contents: ' + extractedFilePath;
        rimraf(extractedFilePath);

        // Try and determine main ROM file
        stage = 'Trying to determine the main ROM file'
        const roms = possibleRoms.map(e => cleanName(cleanPath(e)));
        if (roms.length > 1) {
            return undefined;
        } else if (roms.length === 1) {
            return roms[0];
        }
    } catch (e) {
        log.error(slug, e, stage);
    }
}

/**
 * Helper function to get the file name and extension from a file path.
 * @param {string} p - The file path.
 * @returns {string} The file name with the extension.
 */
function cleanPath(p) {
    return path.basename(p);
}

/**
 * Helper function to lower case, remove all spaces, and special characters from a name.
 * @param {string} n - The name to clean.
 * @returns {string} The cleaned name.
 */
function cleanName(n) {
    return n.toLowerCase().replace(/[\s\/]/g, '-').replace(/[^\w\-\.]/g, '');
}

/**
 * Helper function to asynchronously download a file from a url.
 * @param {string} url - The url to download.
 * @param {string} dest - The file path to put the downloaded file.
 * @returns {Promise} Promise that will resolve when the download is complete.
 */
function download(url, dest) {
    return new Promise((resolve, reject) => {
        const file = fs.createWriteStream(dest);
        http.get(url, function (response) {
            response.pipe(file);
            file.on('finish', function () {
                file.close(() => {
                    resolve();
                });
            });
        }).on('error', function (err) { // Handle errors
            fs.unlink(dest); // Delete the file async. (But we don't check the result)
            if (err) {
                log.error(url, err, dest);
                reject(err.message);
            }
        });
    });
}

/**
 * Helper function to synchronously remove the contents of a directory.
 * @param {string} dirPath - The directory path.
 */
function rimraf(dirPath) {
    if (fs.existsSync(dirPath)) {
        fs.readdirSync(dirPath).forEach(function(entry) {
            var entryPath = path.join(dirPath, entry);
            if (fs.lstatSync(entryPath).isDirectory()) {
                rimraf(entryPath);
            } else {
                fs.unlinkSync(entryPath);
            }
        });
        fs.rmdirSync(dirPath);
    }
}
