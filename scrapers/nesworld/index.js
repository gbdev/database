const meta = require('./meta');
const filesystem = require('./filesystem');

meta.gather('http://www.nesworld.com/article.php?system=gbc&data=gbchomebrew')
    .then(filesystem.push);