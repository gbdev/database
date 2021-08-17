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
DEBUG = True            # enable if you want a more detailed log, beta folder and other useful things 
CLEANZIP = True         # enable if you want to delete downloaded zip file 
BETA_FOLDER = "beta"    # warning: this must not be blank. If you dont want to use this simply set DEBUG to False
TMP_FOLDER = "tmp"      # warning: this must not be blank. It is used to store tmp files.

logger = Logger()

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

def build(prod: Production, entrypath: str):
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

                # fetching rom name in the unzippedfolder
                if prod.platform == "GB":
                    suffix = "gb"
                    path = find("*.gb", filepath + "unzippedfolder")
                elif prod.platform == "GBC":
                    suffix = "gbc"
                    path = find("*.gbc", filepath + "unzippedfolder")
                elif prod.platform == "GBA":
                    suffix = "gba"
                    path = find("*.gba", filepath + "unzippedfolder")
                else:
                    # manage the unknown extensions
                    path = []
                    logger.write("[WARN]"," extension is " + prod.platform + ", unable to manage this extension\n")


                # proper renaming and moving the file
                if path != []:
                    os.rename(path[0], filepath + prod.slug + "." + suffix)
                else:
                    logger.write("[WARN]"," cant rename file")
            
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
        r = requests.get(prod.screenshots[0], allow_redirects=True, timeout=None)
        open(filepath + prod.slug + "." + "png", 'wb').write(r.content)
        prod.screenshots[0] = prod.slug + "." + "png"
    else:
        logger.write("[WARN]", "directory already present. Skipping " + prod.slug + "...")
        return 1
    return 0
    
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
