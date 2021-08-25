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
import contextlib
from webptools import dwebp
import imghdr
from PIL import Image

'''
    This is a special m******* script. It works if and only if a certain zip file has been provided.
    This has been made in this way, because scraping everything would have taken too many hours.
    Additionally, websites like gamejolt and itch.io are un-scrapable, resulting in swears and other awful things.
    Technically, they are scrapable, but just with selenium... which it's boring and it will take ages to me to implement it.

    Two lists are present, gb-autom-source (which barely automatize some entries), and gb-manual-source
    that contains path added manually.
    This cost me something like 2 hours.

    If you're reading this, and you are a dev, and you've uploaded your productions on itch.io or any other
    website that doesn't provide a direct link here is a tip for you: ALWAYS UPLOAD YOUR PRODS SOMEWHERE, WHERE
    IT IS POSSIBLE TO HAVE A DIRECT LINK.

    Thanks, have a nice day :) -Dag 
'''


globalgameslist = utils.gimme_global_games_list()   # slug in entries folder
logger = Logger(utils.PREFERRED_OUTPUT)     # logger will print in file or on console depending on params in utils.PREFERRED_OUTPUT --> LOG or CONSOLE

# Default: "../../entries
entrypath = "py_common/" + utils.BETA_FOLDER + "/" if utils.DEBUG else "../../entries"
unzipped_source =  "py_common/" + utils.TMP_FOLDER + "/"

# unzip the source file
try:
    with zipfile.ZipFile(unzipped_source + "gb-thread-entries.zip","r") as zip_ref:
        zip_ref.extractall(unzipped_source)
except zipfile.error as e:
    print("[ERR] " + e)
    exit(1)

def build(prod: Production, entrypath: str, desired_extentions: list):
    '''
        given a prod "Production" object containing
        all production's data, create a proper named folder, fetches all files (screenshot + rom)
        and properly organize everything 
    '''
    if not os.path.exists(entrypath + prod.slug):
        #############
        # PROD FILE #
        #############
        # make its own folder
        os.mkdir(entrypath + prod.slug, 0o777)

        # figuring out the suffix
        suffix = str.lower(prod.url.split(".")[-1])

        # building the filepath
        filepath = entrypath + prod.slug + "/"
        
        # unzip in case of zip
        if prod.url.endswith(".zip") or prod.url.endswith(".ZIP"):
            # download and unzip

            logger.write("[INFO]", " Unzipping zip file: " + prod.url)

            try:
                with zipfile.ZipFile(unzipped_source + "gb-thread-entries/gb-manual-dir/" + prod.url,"r") as zip_ref:
                    zip_ref.extractall(filepath + "unzippedfolder")

                # manage all extensions, and it doesn't matter if they have uppercase or lowercase
                path = []       # eventually the file
                
                extentions = utils.fix_extentions(desired_extentions)
                for extension in extentions:
                    path = utils.find("*." + extension, filepath + "unzippedfolder")
                    if path != []:
                        break
                
                # proper renaming and moving the file
                if path != []:
                    logger.write("[INFO]", " Renaming from " + path[0] + " to " + (filepath + prod.slug + "." + extension.lower()) + "...")
                    os.rename(path[0], filepath + prod.slug + "." + extension.lower())

                    filename = []
                    filename.append(prod.slug + "." + path[0].split(".")[-1].lower())
                    prod.files = filename.copy()
                else:
                    logger.write("[WARN]",prod.title + " extension is not a " + prod.platform + " file.")
                    shutil.rmtree("py_common/" + utils.BETA_FOLDER + "/" + prod.slug)
                    return 1

                # cleaning up unneeded files
                shutil.rmtree(filepath + "unzippedfolder")
                if utils.CLEANZIP: os.remove(unzipped_source + "gb-thread-entries/gb-manual-dir/" + prod.url)
            except zipfile.BadZipFile as e:
                logger.write("[ERR] ", str(e) + " bad zip file")
                shutil.rmtree(entrypath + prod.slug)
                return 1
        else:
            # it is a proper gb file -> just write the filename in its own structure field
            logger.write("[INFO]", " Renaming from " + unzipped_source + "gb-thread-entries/gb-manual-dir/" + prod.url + 
            " to " + "py_common/" + utils.BETA_FOLDER + "/" + prod.slug + "/" + prod.slug + "." + suffix + "...")
            os.rename(  unzipped_source + "gb-thread-entries/gb-manual-dir/" + prod.url, 
                        "py_common/" + utils.BETA_FOLDER + "/" + prod.slug + "/" + prod.slug + "." + suffix)


        # update production object file
        prod.files = []
        prod.files.append(prod.slug + "." + suffix)
        
        if prod.screenshots and prod.screenshots[0] != "None":
            # download the screenshot
            logger.write("[INFO]", " Downloading screenshot...") 
            
            r = requests.get(prod.screenshots[0], allow_redirects=True, timeout=None)

            # figuring out what kind of screenshots I am dealing with
            screen_file_path = filepath + prod.slug + "."
        
            # screenshot fileext
            screen_ext = prod.screenshots[0].split(".")[-1]
            logger.write("[INFO]", " The screenshot is in " + screen_ext + " format")

            if screen_ext.lower() == "png":
                screen_file_path += "png"
            else:
                screen_file_path += screen_ext

            open(screen_file_path, 'wb').write(r.content)
            
            if screen_ext != "png":
                im = Image.open(screen_file_path).convert("RGB")
                im.save(filepath + prod.slug + ".png", "png")
                
                logger.write("[INFO]", " Screenshot has been converted into a PNG file.")
                logger.write("[INFO]", " Removing screenshot " + screen_ext + " file...")

                os.remove(screen_file_path)
            prod.screenshots[0] = prod.slug + "." + "png"
        else:
            logger.write("[INFO]", " There is no screenshot for this production!") 
            prod.screenshots = []
    else:
        logger.write("[WARN]", "directory already present. Skipping " + prod.slug + "...")
        return 1
    return 0

def makeJSON(prod, entrypath):
    '''
        build the json file contained in each directory
    '''
    if os.path.exists(entrypath + prod.slug):
        if prod.screenshots != []:
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
            "screenshots": [
                prod.screenshots[0],
            ],
            "slug": prod.slug,
            "title": prod.title,
            "typetag": prod.typetag
        }
        else:
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
                "screenshots": [
                ],
                "slug": prod.slug,
                "title": prod.title,
                "typetag": prod.typetag
            }

        utils.updateJSON(jsondata, entrypath + prod.slug + "/game.json")
    else:
        logger.write("[ERR]", "Unable to create file for " + prod.slug + ". There is no directory for this prod.")
        return 1
    return 0


def sources(type_of_source, path):
    fd = open(path)
    lines = fd.readlines()
    lines = [line.strip() for line in lines]


    for l in lines:
        data = l.split(",")

        platform = data[0].upper()
        dev = data[1]
        name = data[2]
        slug = utils.build_slug(name)
        typetag = "game"
        
        screenshot = []
        if data[5] != "None":
            screenshot.append(data[5])
        else:
            screenshot.append("None")
        

        logger.write("[INFO]", " Building " + name + " - " + slug + "...")

        if data[4].endswith(".rar"):
            logger.write("[ERR]", " Can't deal with rar files." + data[4])
            continue


        if type_of_source.upper() == "AUTO":
            prod = Production(name, slug, dev, platform.upper(), typetag, screenshot, [None], url=data[4])
            
            utils.build(prod, entrypath, ["GB", "GBC"])

            logger.write("[INFO]", " Making JSON... ")
            makeJSON(prod, entrypath)
            
        else:
            prod = Production(name, slug, dev, platform.upper(), typetag, screenshot, [None], url=data[4])
            
            build(prod, entrypath, ["GB", "GBC"])
            
            logger.write("[INFO]", " Making JSON... ")
            makeJSON(prod, entrypath)

def main():
    # sigh, I can't believe I am doing this...
    # semi-automatic entries
    logger.write("[INFO]", " Building from semi-automatic sources...")
    sources("AUTO", unzipped_source + "gb-thread-entries/gb-autom-source")

    logger.write("[INFO]", " Building from manual sources...")
    sources("MANUAL", unzipped_source + "gb-thread-entries/gb-manual-source")

    # clean
    logger.write("[INFO]"," Removing unzipped_source folder..." + unzipped_source + "gb-thread-entries")
    shutil.rmtree(unzipped_source + "gb-thread-entries")

    logger.write("[INFO]", " Yaronet script has been executed.")

main()