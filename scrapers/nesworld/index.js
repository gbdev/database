const filesystem = require('./filesystem');
const log = require('./log');
const meta = require('./meta');

meta.gather('http://www.nesworld.com/article.php?system=gbc&data=gbchomebrew')
    .then((meta) => {
        log.title('Game List');
        console.log(JSON.stringify(meta.map(m => m.slug).sort()));
        return meta;
    })
    .then(filesystem.push)
    .then(() => {
        log.title('Complete');
    })