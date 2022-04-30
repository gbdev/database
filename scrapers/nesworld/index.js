const filesystem = require('./filesystem');
const log = require('./log');
const meta = require('./meta');

Promise.all([
        meta.gather('http://www.nesworld.com/article.php?system=gb&data=gbhomebrew', 'nswld-dmg'),
        meta.gather('http://www.nesworld.com/article.php?system=gbc&data=gbchomebrew', 'nswld')
    ]).then((meta) => {
        meta = meta.flat();
        log.title('Game List');
        console.log(JSON.stringify(meta.map(m => m.slug).sort()));
        return meta;
    })
    .then(filesystem.push)
    .then(() => {
        log.title('Complete');
    })
