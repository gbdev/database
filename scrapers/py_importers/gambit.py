# dag7 - 2021

'''
    What this script does:
    gambit-prods page is a mess. Not only you will need to scrape everything, but once scraped, roms will be
    in a strange pdb format. gambit-prods provide a link where to download all those roms in a normal gb/gbc format
    in a single zip file.
    This script will download that zip file and it will move every gb file into an appropriate folder, with screenshots
    and game.json
'''

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
logger = Logger(utils.PREFERRED_OUTPUT)
baseurl = "http://www.gambitstudios.com/"

#############
### DEBUG ###
#############
added = []              # debug
#as a friendly reminder, remember to change utils.DEBUG flag!

#################
### CONSTANTS ###
#################
# we first need to download a zip full of roms and manually map every single rom
slug_to_rom = {
    "ant-soldiers":"Ants.gb",
    "breakout":"BREAKOUT.GB",
    "chip-the-chick":"ChipTheChick.gb",
    "dan-laser":"DanLaser.gb",
    "deep-scan":"DeepScan.cgb",
    "hungry-are-the-dead":"HungryAreTheDead.cgb",
    "horrible-demon-ii":"Demon2.gb",
    "falldown":"Falldown.cgb",
    "jetpak-dx":"JetPakDX.cgb",
    "jetset-willy":"JetSetWilly.gb",
    "maze":"Maze.cgb",
    "mines":"Mines.gbc",
    "mousetrap":"Mousetrap.gbc",
    "pak-man":"pakman.GBC",
    "puzzlex":"PuzzleX.gb",
    "sokoban":"sokoban.gb",
    "sqrxz":"SQRXZ.GB",
    "starfisher":"StarFisher.gb",
    "they-came-from-outer-space":"TCFOS.GB"
}

# disable utils.DEBUG flag
# Default: "../../entries
entrypath = "py_common/" + utils.BETA_FOLDER + "/" if utils.DEBUG else "../../entries"  # this means: database/scrapers/py_common/beta/
tmp_zip_path = "py_common/" + utils.TMP_FOLDER + "/"    # this means: database/scrapers/py_common/tmp

#################
### FUNCTIONS ###
#################
# this dude is a though one, I will custom the build function
def custom_build(prod: Production, entrypath: str):
    if not os.path.exists(entrypath + prod.slug):
        # building the filepath
        filepath = entrypath + prod.slug + "/"

        # make its own folder
        os.mkdir(entrypath + prod.slug, 0o777)

        # download the screenshot
        r = requests.get(prod.screenshots[0], allow_redirects=True, timeout=None)
        open(filepath + prod.slug + "." + "png", 'wb').write(r.content)
        prod.screenshots[0] = prod.slug + "." + "png"

        # figuring out the extension and defining product's platform
        ext = ""
        if slug_to_rom[prod.slug].endswith(".gb") or slug_to_rom[prod.slug].endswith(".GB"):
            ext = ".gb"
            prod.platform = "GB"
        if slug_to_rom[prod.slug].endswith(".gbc") or slug_to_rom[prod.slug].endswith(".gbc"):
            ext = ".gbc"
            prod.platform = "GBC"
        if slug_to_rom[prod.slug].endswith(".cgb") or slug_to_rom[prod.slug].endswith(".CGB"):
            ext = ".cgb"
            prod.platform = "GBC"

        # ensures that in game.json, filename is correct
        prod.files.append(prod.slug + ext)

        # rename the file from unzipped zip folder to slug (using the dict)
        os.rename(  "py_common/" + utils.TMP_FOLDER + "/unzippedfolder/" + slug_to_rom[prod.slug],
                    "py_common/" + utils.TMP_FOLDER + "/unzippedfolder/" + prod.slug + ext)

        # move the file from unzipped zip folder to game appropriate folder
        os.rename(  "py_common/" + utils.TMP_FOLDER + "/unzippedfolder/" + prod.slug + ext,
                    filepath + "/" + prod.slug + ext)
    else:
        logger.write("[WARN]", "directory already present. Skipping " + prod.slug + "...")
        return 1
    return 0


def scrape():
    '''
        scrape gambit prods page and fetches all links
        - each link will be processed (scraped) and a Production object will be built
        - this object will be used to build JSON, files and folders
    ''' 
    logger.write("[INFO]", "Scraping gambitprod's website" + "\n")
    page = requests.get(baseurl + "FreeSoftware.asp", timeout=None)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    tables = soup.find_all("table", {"width":"100%", "cellpadding":"4", "border":"1"})
    tds = tables[0].findChildren('td')

    ##############
    ## ZIP FILE ##
    ##############
    # download the zipped file containing all roms
    gb_gambit_roms_url = "http://www.gambitstudios.com/Products/GBFree/freegb.zip"
    r = requests.get(gb_gambit_roms_url, allow_redirects=True, timeout=None, verify=False)
    if r.status_code != 200:
        logger.write("[ERR]:", str(r.status_code) + ": " + gb_gambit_roms_url)
        return 1

    # unzip file
    open(tmp_zip_path + "tmp.zip", 'wb').write(r.content)
    with zipfile.ZipFile(tmp_zip_path + "tmp.zip" ,"r") as zip_ref:
        zip_ref.extractall(tmp_zip_path + "unzippedfolder")

    # remove the tmp.zip
    os.remove(tmp_zip_path + "tmp.zip")
    
    # now GB files are all in py_common/tmp/unzippedfolder 

    #############
    ## PARSING ##
    #############
    # we need to parse from 2 to 21
    for i in range(2, 21):
        screenshots = []
        
        # defining common things
        developer = "Gambit Studios"
        typetag = "game"
        devWebsite = "http://www.gambitstudios.com/"
        
        if (len(tds[i].findChildren('a')) == 1):
            # [<a href="Products/GBFree/puzzlex.zip"><img border="2" src="images/GBFreeware/puzzlex.gif"/></a>]
            # this was a though one: it was un-scrapable
            title = "PuzzleX"
            slug = utils.build_slug("Puzzlex")
            
            screenshots.append(baseurl + str(tds[i].findChildren('a')[0].findChildren("img")[0]['src']))
            
        else:
            title = str(tds[i].findChildren('a')[0].text)
            slug = utils.build_slug(str(tds[i].findChildren('a')[0].text))
            
            screenshots.append(baseurl + str(tds[i].findChildren('a')[1].findChildren("img")[0]['src']))

        # this object will be used to build the file hierarchy
        prod = Production(title, slug, developer, "GB", typetag, screenshots, [], devWebsite=devWebsite)
        
        # check if it could be added to database or not
        # building files
        ret = custom_build(prod, entrypath)

        # make required JSON file
        if ret != 1:
            ret = utils.makeJSON(prod, entrypath)

            # useful to print all added entries (to spot duplicates for example)
            if utils.DEBUG:
                added.append(prod.slug)

def main():
    scrape()

    if utils.DEBUG:
        [ logger.write("[TITLE]", f) for f in added ]

    # cleaning the tmp folder
    shutil.rmtree(tmp_zip_path + "unzippedfolder")

    logger.write("[INFO]", "Gambit importer ended!")    

main()
