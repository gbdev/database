const fs = require('fs');
const jsdom = require('jsdom');
const log = require('./log');
const { JSDOM } = jsdom;

/**
 * Scrape the url and gather game meta for each game presented on the page.
 * @param {string} url - The url to gather the game meta from (really only supports nesworld).
 * @returns {Object[]} An array of game meta objects.
 */
exports.gather = (url, suffix) => {
    const rowsAsync = [];
    log.title('Loading DOM and gathering Meta from: ' + url);
    return JSDOM.fromURL(url)
        .then((dom) => {
            const document = dom.window.document;
            document.querySelectorAll('.CONTENT-DATA > table tbody > tr')
                .forEach((row) => {
                    if (row.childElementCount > 1) {
                        rowsAsync.push(parseRow(row, suffix));
                    }
                });
            return Promise.all(rowsAsync)
                .then((rows) => {
                    let filteredRows = rows.filter(r => !r.exists && (r.rom != null && r.rom.length > 0));
                    filteredRows.forEach((row) => {
                        delete row.exists;
                    });
                    return filteredRows;
                });
        });
}

/**
 * Parse the DOM row from nesworld and build the game meta object.
 * This function is very messy (nesworld has a terrible DOM structure), and is hyper specific to nesworld.
 * @async
 * @param {HTMLElement} row - The game DOM row from nesworld.
 * @returns {Object} A game meta object.
 */
async function parseRow(row, suffix) {
    const meta = {
        title: '',
        slug: '',
        developer: '',
        platform: 'GB',
        typetag: 'homebrew',
        description: '',
        screenshots: [],
        exists: false,
        rom: '',
    };

    const columns = row.childElementCount;
    if (columns === 3) {
        // Screenshots
        meta.screenshots.push(row.querySelector('td:nth-child(1) > img').getAttribute('src'));
        row.querySelectorAll('td:nth-child(2) img').forEach((img) => {
            const src = img.getAttribute('src');
            if (!src.includes('disk_save') && !src.includes('homebrew_noscreenshot')) {
                meta.screenshots.push(src);
            }
        });

        // Rom Link
	const romLink = row.querySelector('td:nth-child(2) center > a');
        meta.rom = romLink != null ? romLink.getAttribute('href') : '';

        let textNodesCount = 0;
        const contentNodes = row.querySelector('td:nth-child(3)').childNodes;
        contentNodes.forEach((node) => {
            switch (node.tagName) {
                // Title
                case 'FONT': {
                    meta.title = node.textContent.trim();
                    break;
                }
                // Developer
                case 'A': {
                    meta.developer = node.textContent.trim();
                    break;
                }
                // #TextNode
                case undefined: {
                    const text = node.textContent.trim();
                    // Developer or just 'By' text
                    if (textNodesCount === 0) {
                        if (text && text !== 'By') {
                            const matches = text.match(/By\s(.*)/);
                            meta.developer = (matches && matches.length > 1) ? matches[1] : 'Unknown';
                        }
                    }
                    // Description
                    else if (textNodesCount === 1) {
                        meta.description = text.trim();
                    }
                    textNodesCount++;
                    break;
                }
            }
        });

        // Type Tag
        if (meta.title.toLowerCase().includes('demo')) {
            meta.typetag = 'demo';
        }
    } else if (columns === 4) {
        // Rom Link
	const romLink = row.querySelector('td:nth-child(2) a');
        meta.rom = romLink != null ? romLink.getAttribute('href') : '';

        // Title
        meta.title = row.querySelector('td:nth-child(3)').textContent.trim();

        //Developer
        meta.developer = row.querySelector('td:nth-child(4)').textContent.trim().substring(3);

        // Type Tag
        if (meta.title.toLowerCase().includes('demo')) {
            meta.typetag = 'demo';
        }
    } else {
        log.error('DOM', null, 'Unexpected number of columns on row in DOM: ' + columns, row);
    }

    // Slug
    if (meta.title) {
        meta.slug = meta.title.toLowerCase().replace(/[\s\/]/g, '-').replace(/[^\w\-]/g, '');
        if (fs.existsSync('../../entries/' + meta.slug)) {
            log.info('Game with slug already exists: ' + meta.slug);
            meta.exists = true;
            meta.slug = meta.slug + '-' + suffix;
        }
    }

    // Clean up
    if (!meta.developer) delete meta.developer;
    if (!meta.description) delete meta.description;

    // Check if screenshots is empty
    if (meta.screenshots.length === 0) {
        log.warn('No screenshots found for: ' + meta.slug + ', adding placeholder.png');
    }

    return meta;
}
