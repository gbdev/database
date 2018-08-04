const http = require('http')
const https = require('https')
const fs   = require('fs')
const URL  = require('url')
const PATH = require('path')
const { pipeline } = require('stream')

const async  = require('async')
const contentDisposition = require('content-disposition')
const jsdom  = require('jsdom/lib/old-api')
const mkdirp = require('mkdirp')

const baseURL = 'https://pdroms.de/files/gameboy/'
const outDir  = PATH.format(PATH.parse('pdroms.de'))

const handleError = function (err) {
	if (err) {
		console.error(err)
		process.exit(1)
	}
}

const processPage = function (url, callback) {
	console.log("Processing page: ", url)

	jsdom.env({
		url: url,
		done: function (err, window) {
			if (err) return callback(err)

			const document = window.document

			document.querySelectorAll('.file_post')

			const links = document.querySelectorAll('.file_post > .post-title > a')
			const nextPage = document.querySelector('.wp-pagenavi > .current + a')

			if (nextPage) {
				pageQueue.push(nextPage.getAttribute('href'), handleError)
			}

			for (let i in links) {
				if (!links.hasOwnProperty(i)) continue

				const link = links[i]
				const href = link.getAttribute('href')
				filePageQueue.push(href, handleError)
			}

			console.log("Processed page:  ", url)
			callback()
			window.close()
		}
	})
}

const pageQueue = async.queue(processPage, 5)
const filePageQueue = async.queue(function (url, callback) {
	console.log("Parsing file info page:", url)

	jsdom.env({
		url: url,
		done: function (err, window) {
			if (err) return callback(err)
			const document = window.document
			const link = document.querySelector('.download_link > a')
			const title = document.querySelector('.post-title-big > a').textContent.trim()
			let thumbnail = document.querySelector('.file_thumb_single > img')
			const author = document.querySelector('.file-meta-data > strong').textContent.trim()
			const description = document.querySelector('.post-content > p').textContent.trim()

			if (thumbnail) {
				if (thumbnail.getAttribute('data-lazy-src')) {
					thumbnail = thumbnail.getAttribute('data-lazy-src')
				}
				else {
					thumbnail = thumbnail.getAttribute('src')
				}
			}

			if (link) {
				const href = link.getAttribute('href')
				fileQueue.push({ url: href, thumbnail, title, author, description }, handleError)
				console.log("Found link:", href)
			}

			callback()
			window.close()
		}
	})
}, 5)

const fileQueue = async.queue(function ({ url, thumbnail, title, author, description }, callback) {
	const request = https.get(url, function (res) {
		let filename = res.headers.date + '.' + res.headers['content-type'].replace(/\//g, '-')
		let folder = 'unknown'

		try {
			const cdHeader = res.headers['content-disposition'].replace(/filename=([^"]+?)(?:;|$)/g, 'filename="$1";').replace(/;$/, '')
			const cd = contentDisposition.parse(cdHeader)
			filename = cd.parameters.filename
			folder = title.trim().replace(/\s/g, '-')
		}
		catch (e) { }

		const dir = PATH.join(outDir, folder)

		const json = {
			title,
			slug: title,
			// license: "No information"
			developer: author,
			// repository: "",
			platform: "GB",
			// typetag: "game",
			// tags: [ ],
			schreenshots: [ ],
			rom: filename,
			description
		}

		async.series([
			(cb) => mkdirp(dir, cb),
			(cb) =>	pipeline(res, fs.createWriteStream(PATH.join(dir, filename)), cb),
			(cb) => { if (!thumbnail) { return cb(); }
				https.get(thumbnail, function (res) {
					const remotePath = URL.parse(thumbnail).path
					const path = PATH.format(PATH.parse(remotePath))
					const file = PATH.basename(path)

					json.schreenshots.push(file)
					pipeline(res, fs.createWriteStream(PATH.join(dir, file)), cb)
				})
			},
			(cb) => fs.writeFile(PATH.join(dir, 'game.json'), JSON.stringify(json, null, 4), cb)
		], callback)
	})
}, 5)

pageQueue.drain = function () {
	console.log("Page Queue Ran Empty!")
}

filePageQueue.drain = function () {
	console.log("File Info Page Queue Ran Empty!")
}

fileQueue.drain = function () {
	console.log("File Queue Ran Empty!")
}

pageQueue.push(baseURL)
