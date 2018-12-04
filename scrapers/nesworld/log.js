const chalk = require('chalk');

/**
 * Log out a title.
 * @param {string} title
 */
exports.title = (title) => {
    console.info();
    console.info(chalk.green('**********'));
    console.info(chalk.green('**  ') + title);
    console.info(chalk.green('**********'));
}

/**
 * Log out a error.
 * @param {string} name
 * @param {Error} exception
 * @param {string[]} messages
 */
exports.error = (name, exception, ...messages) => {
    console.error();
    console.error(chalk.red('Error: '));
    for (let i = 0; i < messages.length; i++) {
        console.error(chalk.red('> ' + messages[i]));
    }
    if (name) {
        console.error(chalk.red('> '), name);
    }
    if (exception) {
        console.error(chalk.red('> '), exception.toString().trim());
    }
    console.error();
}

/**
 * Log out a info message.
 * @param {string} message
 */
exports.info = (message) => {
    console.info(chalk.green('Info: ') + message);
}

/**
 * Log out a warning message.
 * @param {string} message
 */
exports.warn = (message) => {
    console.warn(chalk.yellow('Warn: ') + message);
}