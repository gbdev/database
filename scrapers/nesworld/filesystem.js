const AdmZip = require('adm-zip');
const http = require('http');
const path = require('path');
const fs = require('fs');

const url = 'http://www.nesworld.com/';
const base = path.resolve(__dirname, 'entries');

exports.push = (meta) => {
    if (fs.existsSync(base)) rimraf(base);
    fs.mkdirSync(base);

    const promises = [];
    for (let i = 0; i < meta.length; i++) {
        promises.push(createGame(meta[i]));
    }
    return promises;
}

async function createGame(game) {
    const gamePath = path.resolve(base, game.slug);
    fs.mkdirSync(gamePath);

    // Download Screenshots
    for (let i = 0; i < game.screenshots.length; i++) {
        const screenshotFilename = cleanPath(game.screenshots[i]);
        await download(url + game.screenshots[i], path.resolve(gamePath, screenshotFilename));
        game.screenshots[i] = screenshotFilename;
    }

    // Download ROM zip
    const romZipFilename = cleanPath(game.rom);
    await download(url + game.rom, path.resolve(gamePath, romZipFilename));

    // unzip(path.resolve(gamePath, romZipFilename));

    game.rom = romZipFilename;

    fs.writeFileSync(path.resolve(gamePath, 'game.json'), JSON.stringify(game, null, 4));
}

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
            if (cb) {
                console.error(err.message, url, dest);
                reject(err.message);
            }
        });
    });
};

function unzip(filePath) {
    try {
        const zip = new AdmZip(filePath);
        console.log(zip.getEntries().map(e => e.entryName).filter(name => /.gb(c?)$/g.test(name.toLowerCase())));
    } catch (e) {
        console.error('Error: ', filePath);
    }
    console.log('------------');
}

function cleanPath(p) {
    return p.replace(/.*\//g, '');
}

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

/*
{ title: 'Binary Chaos',
    slug: 'binary-chaos',
    developer: 'Stoic Software',
    platform: 'gbc',
    typetag: 'homebrew',
    description: '',
    screenshots: [ 'gbc/homebrew/pics/bchaosss.png' ],
    rom: 'gbc/homebrew/game/bchaosss.zip' }
*/