# dag7 - 2021

import sys
import re
import os
import json
import shutil
import zipfile
import fnmatch
import urllib3
import requests
import unicodedata
from urllib.request import urlopen
from bs4 import BeautifulSoup

from py_common.Logger import Logger
from py_common.Production import Production
import py_common.utils as utils

########################
### GLOBAL VARIABLES ###
########################
globalgameslist = utils.gimme_global_games_list()   # slug in entries folder
logger = Logger(utils.PREFERRED_OUTPUT)     # logger will print in file or on console depending on params in utils.PREFERRED_OUTPUT --> LOG or CONSOLE

baseurl = "https://pouet.net"
blacklist = [
    "grey-screen-with-no-music", # 22kb zip (empty)
    "dangan-gb-4-trainer",      # corrupted zip
    "altstork-2004-invitation",  # 404, but cant manage it
    "dcs-gbc-intro-7",          # corrupted zip             https://ftp.untergrund.net/users/havoc/POUET/gameboy/DCS-I_06.ZIP
    "beauty-girls-vol-i",
    "fire-gbc",                 # duplicate entry
    "fatass",                   # not a prod -- it is a tool
    "bmp2cgb",                  # not a prod -- it is a tool
    "gejmbaj",                  # rar file, cant deal with it
    "intrinsic-gravelty",       # not a gb production
    "second-reality-gameboy-remix"      # gibberish output file
    "sjasmplus"                 # not a gb file --> it is a tool

]

#############
### DEBUG ###
#############
added = []              # debug
#as a friendly reminder, remember to change utils.DEBUG flag!

#################
### CONSTANTS ###
#################

#TODO: GBA placeholder intentionally left here for future development.
##
    # dict containing pouet's categories,
    # with a mapped "simplified" category according to CONTRIBUTING.MD 
    # "game", "homebrew", "demo" or "hackrom"
##
CATEGORIES = {
    "32b":"demo",
    "64b":"demo",
    "128b":"demo",
    "256b":"demo",
    "512b":"demo",
    "1k":"demo",
    "4k":"demo",
    "8k":"demo",
    "16k":"demo",
    "32k":"demo",
    "40k":"demo",
    "64k":"demo",
    "96k":"demo",
    "100k":"demo",
    "128k":"demo",
    "256k":"demo",
    "artpack":"demo",
    "bbstro":"demo",
    "cracktro":"demo",
    "demo":"demo",
    "demopack":"demo",
    "demotool":"homebrew",
    "dentro":"demo",
    "diskmag":"demo",
    "fastdemo":"demo",
    "game":"game",
    "intro":"demo",
    "invitation":"demo",
    "liveact":"demo",
    "procedural graphics":"demo",
    "report":"demo",
    "slideshow":"demo",
    "votedisk":"demo",
    "wild":"demo"
}

PLATFORMS = {
    "Gameboy":"GB",
    "Gameboy Color":"GBC"
    # "Gameboy Advance":"GBA"
}

# disable utils.DEBUG flag in prod
# Default: "../../entries
entrypath = "py_common/" + utils.BETA_FOLDER + "/" if utils.DEBUG else "../../entries"  # this means: database/scrapers/py_common/pouet_demoscene/

#TODO: Resolve this issue.
print("[WARN]: if a prod is already present in the gamesList with another slugname, two different entries will be created!")

#################
### FUNCTIONS ###
#################
def scrape(platform):    
    '''
        scrape Pouet's prods page and fetches all links
        - each link will be processed (scraped) and a Production object will be built
        - this object will be used to build JSON, files and folders
    ''' 
    for category in CATEGORIES:
        logger.write("[INFO]", "Scraping category " + category )
        page = requests.get(baseurl + "/prodlist.php?type%5B%5D=" + category + "&platform%5B%5D=" + platform + "&page=1", timeout=None)
        soup = BeautifulSoup(page.content, 'html.parser')

        # get total number of pages
        selpages = soup.find("select", {"name":"page"})
        options = selpages.find_all("option")
        
        if options == []: continue  # in case of empty page
        
        numberofpages = int(options[-1].text)
        logger.write("[INFO]", "Total number of pages: " + str(numberofpages) )

        # parsing every page
        for i in range(0, numberofpages):
            logger.write("[INFO]", "Parsing page: " + str(i+1) )
            #TODO: dont call twice this page, as it is called before
            
            page = requests.get(baseurl + "/prodlist.php?type%5B%5D=" + category + "&platform%5B%5D=" + platform + "&page=" + str(i+1), timeout=None)
            soup = BeautifulSoup(page.content, 'html.parser')

            # get the big prods table
            prodTable = soup.findAll('table')[1].findAll('tr')
            
            # get rows; for each rows, get the name of the prod and the internal link
            for tr in prodTable:
                tds = tr.find_all('td')
                if tds:
                    for td in tds:
                        spans = td.find_all("span", {"class": "prod"}, recursive=False)
                        for span in spans:
                            if span:
                                a = span.findChildren()[0]
                                pouet_internal_link = baseurl + "/" + a.get("href")
                                
                                # building slug: all lowercase, each word separated by hyphen, no special character
                                slug = utils.build_slug(a.text)
                                
                                # scrape pouet's page: the returned object will be used to build the file hierarchy
                                prod = scrape_page(slug, pouet_internal_link, platform)

                                #DBGPRINT slugprint
                                #print(prod.slug)

                                # check if it could be added to database or not
                                if prod.slug not in globalgameslist and prod.slug not in blacklist:
                                    # building files
                                    ret = utils.build(prod, entrypath, list(PLATFORMS.values()))

                                    # make required JSON file
                                    if ret != 1:
                                        ret = utils.makeJSON(prod, entrypath)
                                        
                                        # useful to print all added entries (to spot duplicates for example)
                                        if utils.DEBUG:
                                            added.append(prod.slug)
                                else:
                                    logger.write("[WARN]", prod.slug + " either in blacklist or already in entries folder!")


                    

def scrape_page(slug, url, platform):
    '''
        given a slug and Pouet production url, it returns an object containing everything useful
        to build a file hierarchy
    '''
    # init variables ( if not, lil' python cries :/ )
    screenshots = []
    files = []
    typetag = ""

    page = requests.get(url, timeout=None)
    soup = BeautifulSoup(page.content, 'html.parser')

    # get the prod data table
    table = soup.find('table', id="pouetbox_prodmain")
    
    # get rows; for each rows, get the name of the prod and the internal link
    prodheader = soup.find('span', id="title")

    # fetching title
    title = prodheader.find('span', id="prod-title").text
    
    # fetching developer
    a_children = prodheader.findChildren()
    if 1 < len(prodheader.findChildren()):
        developer  = a_children[1].text
    else:   # if developer not properly specified, take the first person credited in the page
        credited_dev = soup.select("#credits > ul:nth-child(1) > li:nth-child(1) > a:nth-child(2)")
        if 0 < len(credited_dev):
            developer = credited_dev[0].text
        else:
            # in this case, credits appear nowhere
            developer = "unknown"

    # fetching tag
    spans = soup.find_all("span", {"class": "type"})
    for span in spans:
        typetag = CATEGORIES[span.text]
        break   # avoiding multiple tags: it takes just the first one (multiple tags example: https://www.pouet.net/prod.php?which=59196)
    
    # fetching screenshot
    screenshottd = table.find('td', id="screenshot")
    screenshots.append(screenshottd.findChildren()[0]['src'])

    # fetching download link: regex has been used because if not, it won't download any file (view it is just a landing page)
    url = table.find('a', id="mainDownloadLink").get('href')
    url = re.sub("https://files.scene.org/view/", "https://files.scene.org/get/", url)
    
    # fetching source link (if present)
    source = soup.find(lambda tag: tag.name == "a" and "source" in tag.text.lower())
    source = source.get("href") if source else ""
    
    # fetching video
    video = soup.find(lambda tag: tag.name == "a" and "youtube" in tag.text.lower())
    video = video.get("href") if video else ""
    
    return Production(title, slug, developer, PLATFORMS[platform], typetag, screenshots, files, video, repository=source, url=url)

def main():
    for platform in PLATFORMS.keys():
        logger.write("[INFO]","Parsing platform: " + platform)
        scrape(platform)
    
main()

if utils.DEBUG:
    [ logger.write("[TITLE]", f) for f in added ]

logger.write("[INFO]", "Pouet importer ended!")