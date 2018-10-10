const filesystem = require('./filesystem');
const log = require('./log');
const meta = require('./meta');

meta.gather('http://www.nesworld.com/article.php?system=gbc&data=gbchomebrew')
    .then(filesystem.push)
    .then(() => {
        log.title('Complete');
    })