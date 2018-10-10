const chalk = require('chalk');

exports.title = (title) => {
    console.info();
    console.info(chalk.green('**********'));
    console.info(chalk.green('**  ') + title);
    console.info(chalk.green('**********'));
}

exports.error = (name, exception, ...messages) => {
    console.error();
    console.error(chalk.red('Error: '));
    for (let i = 0; i < messages.length; i++) {
        console.error(chalk.red('> ' + messages[i]));
    }
    if (exception) {
        console.error(chalk.red('> '), exception)
    }
    console.error();
}

exports.info = (message) => {
    console.info(chalk.green('Info: ') + message);
}

exports.warn = (message) => {
    console.warn(chalk.yellow('Warn: ') + message);
}