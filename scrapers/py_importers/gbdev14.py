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

baseurl = "https://github.com/gbdev/database/files/2202719/gbdev2014-allroms.zip"
blacklist = [
]

#############
### DEBUG ###
#############
added = []              # debug
#as a friendly reminder, remember to change utils.DEBUG flag!

#################
### CONSTANTS ###
#################
# disable utils.DEBUG flag in prod
# Default: "../../entries
entrypath = "py_common/" + utils.BETA_FOLDER + "/" if utils.DEBUG else "../../entries"  # this means: database/scrapers/py_common/beta/

#################
### FUNCTIONS ###
#################
def download():
    '''
        download the zip file containing all the prods
    '''
    r = requests.get(baseurl, allow_redirects=True, timeout=None, verify=False)
    if r.status_code != 200:
        logger.write("[ERR]:", str(r.status_code))

        # cleaning in case of error
        shutil.rmtree("py_common/" + utils.TMP_FOLDER)
        return 1
    
    open("py_common/" + utils.TMP_FOLDER + "/gbdev14.zip", 'wb').write(r.content)


def unzip():
    try:
        # unzip
        with zipfile.ZipFile("py_common/tmp/gbdev14.zip","r") as zip_ref:
            zip_ref.extractall("py_common/tmp/unzippedfolder")
    except zipfile.BadZipFile as e:
        logger.write()("There was a problem with zip file")
        exit(1)

def makeJSON(path, prod):
    '''
        build the json file contained in each directory
    '''
    if os.path.exists(path):
        jsondata = {
            "developer": prod.developer,
            "files": [
                {
                    "default": True,
                    "filename": prod.files[0],
                    "playable": True
                }
            ],
            "platform": prod.platform,
            "repository": prod.repository,
            "screenshots": 
                [ screen for screen in prod.screenshots ]
            ,
            "slug": prod.slug,
            "title": prod.title,
            "typetag": prod.typetag
        }

        utils.updateJSON(jsondata, path + "game.json")
    else:
        logger.write("[ERR]", "Unable to create file for " + prod.slug + ". There is no directory for this prod." + path)
        return 1
    return 0

def figure_out_the_dev(slug):
    '''
        given a slug, return its author.
        Mapped manually.
    '''

    if slug == "bleep":
        return "Sanqui"

    if slug == "back-to-color":
        return "AntonioND"

    if slug == "shmup":
        return "kresna"
    
    if slug == "slider":
        return "Jaeden Amero"
    
    if slug == "steinsgate-8-bit-v0-40":
        return "calc84maniac"

    if slug == "turtlepuzzle":
        return "UraKn0x"

    return ""


def main():
    download()  # download the zip file
    unzip()     # unzip the zip file

    tmp_path = "py_common/" + utils.TMP_FOLDER + "/"
    os.remove(tmp_path + "unzippedfolder/readme.txt")
    shutil.move(tmp_path + "unzippedfolder/snake", tmp_path + "unzippedfolder/gbdev14-snake") # this is necessary, otherwise it will create conflicts
    
    for dir_name in os.listdir(tmp_path + "unzippedfolder"):
        if dir_name == "snake":
            dir_name = "gbdev14-snake"

        # cycle every possible ext until you find (or not) the file
        for ext in utils.fix_extentions(["GB", "GBC"]):
            path = utils.find("*." + ext, tmp_path + "unzippedfolder/" + dir_name)
            if path != []:
                break

        if path == []:
            logger("[ERR]", "Prod " + dir_name + " has no gb/gbc file. Skipping...")
            continue
    

        # fetch list of screenshots
        screenshots = []
        screenshots.append("screen1.png")
        if(os.path.isfile(tmp_path + "unzippedfolder/" + dir_name + "/screen2.png")):
            screenshots.append("screen2.png")
            if os.path.isfile(tmp_path + "unzippedfolder/" + dir_name + "/screen3.png"):
                screenshots.append("screen3.png")
        
        # take filename from path
        files = []

        files.append(path[0].split("/")[-1])

        title = dir_name.replace("_", " ")
        slug = utils.build_slug(title)
        prod = Production(title, slug, figure_out_the_dev(slug), "GB", "game", screenshots, files)
        
        # check if it could be added to database or not
        if prod.slug not in globalgameslist and prod.slug not in blacklist:
            ret = makeJSON(tmp_path + "/unzippedfolder/" + dir_name + "/", prod)
                
            # useful to print all added entries (to spot duplicates for example)
            if utils.DEBUG and ret != 1:
                added.append(dir_name)
        else:
            logger.write("[WARN]", prod.slug + " either in blacklist or already in entries folder!")
            shutil.rmtree(tmp_path + "unzippedfolder/" + dir_name)

    # moving from unzipped folder to beta_folder
    for directory in os.listdir(tmp_path + "unzippedfolder/"):
        if os.path.exists(entrypath + directory):
            shutil.rmtree(entrypath + directory)
        
        shutil.move(tmp_path + "unzippedfolder/" + directory, entrypath + directory)

    # cleaning up unneeded files
    shutil.rmtree(tmp_path)

    if utils.DEBUG:
        [ logger.write("[TITLE]", f) for f in added ]
        logger.write("[INFO]", "GBDev14 importer ended!")

main()
