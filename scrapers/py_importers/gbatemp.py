# dag7 - 2021

# Main list:
# https://gbatemp.net/download/categories/homebrew.1401/

# Each entry:
# https://gbatemp.net/download/slug.internal-number/

import re
import requests
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

from py_common.Logger import Logger
from py_common.Production import Production
import py_common.utils as utils

########################
### GLOBAL VARIABLES ###
########################
# logger will print in file or on console depending on params in utils.PREFERRED_OUTPUT --> LOG or CONSOLE
logger = Logger(utils.PREFERRED_OUTPUT)

baseurl = "https://gbatemp.net"
blacklist = {
    "gb-and-gbc-homebrew-collection": "it is the same found on zophar, and it is a huge list of unsorted files",
    "flappybird": "host is known to be closed (filetrip.net)"
}

#############
### DEBUG ###
#############
added = []              # debug

# as a friendly reminder, remember to change utils.DEBUG flag!
# disable utils.DEBUG flag in prod
# Default: "../../entries
entrypath = "py_common/" + utils.BETA_FOLDER + \
    "/" if utils.DEBUG else "../../entries"


headers = {'User-Agent': 'Mozilla/5.0'}

###############
### METHODS ###
###############


def scrape():
    '''
        scrape Gbatemp prods page and fetches all links
        - each link will be processed (scraped) and a Production object will be built
        - this object will be used to build JSON, files and folders
    '''
    logger.write("[INFO]", "Scraping GB and GBC entries ")
    page = requests.get(
        baseurl + "/download/categories/homebrew.1401/", timeout=None, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # get total number of pages
    link_pages = soup.find_all(
        "a", {"data-tp-primary": "on"}, href=re.compile("/download"))

    logger.write("[INFO]", "Total number of pages: " + str(len(link_pages)))

    # parsing every entry
    for i in range(0, len(link_pages)):
        slug = utils.build_slug(
            link_pages[i]['href'].split("/")[2].split(".")[0])
        prod_url = baseurl + link_pages[i]['href']

        logger.write("[INFO]", "Parsing entry: " +
                     prod_url)

        if slug in blacklist:
            logger.write("[WARN]", "Skipping entry: " +
                         slug + " - reason: " + blacklist[slug])
            continue

        page = requests.get(
            prod_url, headers=headers, timeout=None)
        soup = BeautifulSoup(page.content, 'html.parser')

        developer = soup.findAll('dl')[0].findAll('dd')[0].text
        date = soup.findAll('dl')[3].findAll('dd')[0].text
        date = str(datetime.strptime(date, '%b %d, %Y')).split(" ")[0]

        description = soup.find_all(
            "div", {"block-body", "lbContainer", "js-resourceBody"})[0].find_all('div', {"bbWrapper"})[0].text.replace("\n", " ").strip()

        title = soup.find(
            "h1", {"p-title-value"})
        title = (title.text.strip().replace("\t", "?").split("?")[0]).strip()

        # to request just the file, append /download at the end of its link
        p = Production(title, slug, developer, "gb", "",
                       [], [slug+".gb"], "", url=prod_url+"/download", description=description)
        utils.build(p, entrypath, ["gb", "gbc"])
        utils.makeJSON(p, entrypath)


def main():
    logger.write(
        "[INFO]", "GBATemp scraper! Prods are being downloaded...")
    scrape()

    logger.write("[INFO]", " Gbatemp importer has been executed.")


main()
