import sys
import py_common.utils
import re
import json
import shutil
import zipfile
import fnmatch
import urllib3
import requests
import unicodedata
import contextlib
import urllib
from urllib.request import urlopen
import imghdr
from PIL import Image

import os
from os import listdir
from os.path import isfile, join

from bs4 import BeautifulSoup
from unidecode import unidecode

from py_common.Logger import Logger
from py_common.Production import Production

###########################
### GLOBAL VAR AND CONS ###
###########################
DEBUG = True                    # enable if you want a more detailed log, beta folder and other useful things 
CLEANZIP = True                 # enable if you want to delete downloaded zip file 
BETA_FOLDER = "beta"            # warning: this must not be blank. If you dont want to use this simply set DEBUG to False
TMP_FOLDER = "tmp"              # warning: this must not be blank. It is used to store tmp files.
PREFERRED_OUTPUT = "CONSOLE"    # change it to LOG if you need to output everything in log.txt file
DONT_CARE_EXT = True            # dont care if it is a GB file while scraping GBC (or viceversa), put it in a folder anyway

logger = Logger(PREFERRED_OUTPUT)

# required: we need to check if BETA_FOLDER and TMP_FOLDER exist or not
if not BETA_FOLDER or not TMP_FOLDER or BETA_FOLDER == "" or TMP_FOLDER == "":
    print("BETA_FOLDER or TMP_FOLDER can't be empty!")
    exit(1)
if not os.path.isdir("py_common/" + BETA_FOLDER):
    os.mkdir("py_common/" + BETA_FOLDER)
if not os.path.isdir("py_common/" + TMP_FOLDER):
    os.mkdir("py_common/" + TMP_FOLDER)

#################
### FUNCTIONS ###
#################
# return a proper built slug
def build_slug(slug: str):
    '''
        a slug it is built in this way:
            - removes all special characters, except for letters
            - makes everything lowercase
            - hyphens are used instead of spaces
            - accented characters are normalized (ascii)
    '''
    # delete characters not needed in the slug
    slug = re.sub("[^0-9a-zA-ZÀ-ÖØ-öø-ÿ]+", " ", slug)  # removes all except letters and numbers
    slug = slug.lower() # to lowercase
    slug = slug.strip().replace(" ", "-") # hypens instead of spaces
    slug = unidecode(slug)  # normalize accented characters

    return slug

def find(pattern, path):
    '''
        find files matching a path in a folder and its subfolders
    '''
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))

    return result

def gimme_global_games_list():
    '''
        return a list containing all slugs in entrypath 
    '''
    entries_list = listdir("../../entries")
    
    return(sorted(entries_list + listdir("py_common/" + BETA_FOLDER)) if DEBUG else sorted(entries_list))

def fetch_prod_name(prod, suffix, filepath):
    '''
        return a list with path as the first entry if file is found in the unzippedfolder
        if DONT_CARE_EXT is enabled, it will search if there is a file with a certain extension
        regardless what it's scraping
    '''
    path = []           # manage the unknown extensions

    # fetching product path in the unzippedfolder
    if DONT_CARE_EXT:
        path = find("*." + suffix, filepath + "unzippedfolder")
    else:
        if prod.platform == suffix.upper():     # e.g. if "GB" == "GB"
            path = find("*." + suffix, filepath + "unzippedfolder")
    
    return path

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
        
        # download the file
        # in case of http
        if prod.url.startswith("http"):
            r = requests.get(prod.url, allow_redirects=True, timeout=None, verify=False)
            if r.status_code != 200:
                logger.write("[ERR]:", str(r.status_code) + ": " + prod.slug + " - " + prod.url)

                # cleaning in case of error
                shutil.rmtree(entrypath + prod.slug)
                return 1
            
            open(filepath + prod.slug + "." + suffix, 'wb').write(r.content)
        else:
            with contextlib.closing(urllib.request.urlopen(prod.url)) as r:
                with open(filepath + prod.slug + "." + suffix, 'wb') as f:
                    shutil.copyfileobj(r, f)
        
        # unzip in case of zip
        if prod.url.endswith(".zip") or prod.url.endswith(".ZIP"):
            # download and unzip
            try:
                with zipfile.ZipFile(filepath + prod.slug + "." + suffix,"r") as zip_ref:
                    zip_ref.extractall(filepath + "unzippedfolder")

                # manage all extensions, and it doesn't matter if they have uppercase or lowercase
                path = []       # eventually the file
                
                extentions = fix_extentions(desired_extentions)
                for extension in extentions:
                    path = fetch_prod_name(prod, extension, filepath)
                    if path != []:
                        break
                
                # proper renaming and moving the file
                if path != []:
                    os.rename(path[0], filepath + prod.slug + "." + extension.lower())
                    filename = []
                    filename.append(prod.slug + "." + extension.lower())
                    prod.files = filename
                else:
                    logger.write("[WARN]",prod.title + " extension is not a " + prod.platform + " file.")
                    shutil.rmtree(entrypath + prod.slug)
                    return 1

                # cleaning up unneeded files
                shutil.rmtree(filepath + "unzippedfolder")
                if CLEANZIP: os.remove(filepath + prod.slug + "." + "zip")
            except zipfile.BadZipFile as e:
                logger.write("[ERR] ", str(e) + " bad zip file")
                shutil.rmtree(entrypath + prod.slug)
                return 1
        else:
            # it is a proper gb file -> just write the filename in its own structure field
            pass
        
        # update production object file
        prod.files.append(prod.slug + "." + suffix)
        
        # download the screenshot
        if prod.screenshots[0] != "None":
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

            open(filepath + prod.slug + "." + "png", 'wb').write(r.content)
            prod.screenshots[0] = prod.slug + "." + "png"
        else:
            prod.screenshots = []
            logger.write("[INFO]", "Screenshot not present for this production")
    else:
        logger.write("[WARN]", "directory already present. Skipping " + prod.slug + "...")
        return 1
    return 0

def fix_extentions(desired_extentions):
    '''
        given a theorical list of extensions, it returns a list containing additional correct extensions (like CGB, AGB)
        in this way, we deals with these kind of files
    '''
    final_list = []

    if "GB" in desired_extentions:
        final_list.append("GB")
        final_list.append("gb")

    if "GBC" in desired_extentions:
        final_list.append("GBC")
        final_list.append("gbc")
        final_list.append("CGB")
        final_list.append("cgb")

    if "GBA" in desired_extentions:
        final_list.append("GBA")
        final_list.append("gba")
        final_list.append("AGB")
        final_list.append("agb")

    return final_list
    
def makeJSON(prod, entrypath):
    '''
        build the json file contained in each directory
    '''
    if os.path.exists(entrypath + prod.slug):
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

        updateJSON(jsondata, entrypath + prod.slug + "/game.json")
    else:
        logger.write("[ERR]", "Unable to create file for " + prod.slug + ". There is no directory for this prod.")
        return 1
    return 0

def updateJSON(data, path):
    jsonstr = json.dumps(data, sort_keys=True, indent=4)
    jsonfile = open(path, "w")
    jsonfile.write(jsonstr)
    jsonfile.close()
