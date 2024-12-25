import re
import json
import shutil
import zipfile
import fnmatch
import requests
import contextlib
import urllib
from PIL import Image

import os
from os import listdir

from unidecode import unidecode

from py_common.Logger import Logger
import py7zr

###########################
### GLOBAL VAR AND CONS ###
###########################
# enable if you want a more detailed log, beta folder and other useful things
DEBUG = True
CLEANZIP = True  # enable if you want to delete downloaded zip file
# warning: this must not be blank. If you dont want to use this simply set DEBUG to False
BETA_FOLDER = "beta"
# warning: this must not be blank. It is used to store tmp files.
TMP_FOLDER = "tmp"
# change it to LOG if you need to output everything in log.txt file
PREFERRED_OUTPUT = "CONSOLE"
# dont care if it is a GB file while scraping GBC (or viceversa), put it in a folder anyway
DONT_CARE_EXT = True

logger = Logger(PREFERRED_OUTPUT)
headers = {"User-Agent": "Mozilla/5.0"}

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
    """
    a slug it is built in this way:
        - removes all special characters, except for letters
        - makes everything lowercase
        - hyphens are used instead of spaces
        - accented characters are normalized (ascii)
    """
    # delete characters not needed in the slug
    # removes all except letters and numbers
    slug = re.sub("[^0-9a-zA-ZÀ-ÖØ-öø-ÿ]+", " ", slug)
    slug = slug.lower()  # to lowercase
    slug = slug.strip().replace(" ", "-")  # hypens instead of spaces
    slug = unidecode(slug)  # normalize accented characters

    return slug


def find(pattern, path):
    """
    find files matching a path in a folder and its subfolders
    """
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))

    return result


def gimme_global_games_list():
    """
    return a list containing all slugs in entrypath
    """
    entries_list = listdir("../../entries")

    return (
        sorted(entries_list + listdir("py_common/" + BETA_FOLDER))
        if DEBUG
        else sorted(entries_list)
    )


def fetch_prod_name(prod, suffix, filepath):
    """
    return a list with path as the first entry if file is found in the unzippedfolder
    if DONT_CARE_EXT is enabled, it will search if there is a file with a certain extension
    regardless what it's scraping
    """
    path = []  # manage the unknown extensions

    # fetching product path in the unzippedfolder
    if DONT_CARE_EXT:
        path = find("*." + suffix, filepath + "unzippedfolder")
    else:
        if prod.platform == suffix.upper():  # e.g. if "GB" == "GB"
            path = find("*." + suffix, filepath + "unzippedfolder")

    return path


def build(prod, entrypath: str, desired_extensions: list):
    """
    Given a prod "Production" object containing
    all production's data, create a properly named folder, fetch all files (screenshot + ROM),
    and organize everything.
    """
    # Create folder if not already present
    target_folder = os.path.join(entrypath, prod.slug)
    if not os.path.exists(target_folder):
        os.mkdir(target_folder, 0o777)

        # Extract file extension
        suffix = prod.url2.split(".")[-1].lower()

        if suffix not in desired_extensions and suffix not in ["zip", "7z", "mp4"]:
            print(f"ERROR: {prod.slug} extension is not in {desired_extensions}")
            suffix = "gb"  # Fallback extension

        # Build the file path
        filepath = os.path.join(target_folder, f"{prod.slug}.{suffix}")

        # Download the file
        try:
            if prod.url.startswith("http"):
                r = requests.get(
                    prod.url, allow_redirects=True, timeout=None, verify=False
                )
                if r.status_code != 200:
                    raise Exception(f"HTTP Error {r.status_code}")
                with open(filepath, "wb") as f:
                    f.write(r.content)
            else:
                with contextlib.closing(urllib.request.urlopen(prod.url)) as r:
                    with open(filepath, "wb") as f:
                        shutil.copyfileobj(r, f)
        except Exception as e:
            logger.write("[ERR]:", f"Error downloading {prod.slug}: {e}")
            shutil.rmtree(target_folder)
            return 1

        # Unzip and handle files
        if suffix in ["zip", "7z"]:
            unzipped_path = os.path.join(target_folder, "unzippedfolder")
            os.makedirs(unzipped_path, exist_ok=True)

            try:
                if suffix == "zip":
                    with zipfile.ZipFile(filepath, "r") as zip_ref:
                        zip_ref.extractall(unzipped_path)
                elif suffix == "7z":
                    with py7zr.SevenZipFile(filepath, mode="r") as z:
                        z.extractall(unzipped_path)
            except Exception as e:
                logger.write("[ERR]:", f"Failed to extract {suffix} file: {e}")
                shutil.rmtree(target_folder)
                return 1

            # Search for desired extensions in the extracted folder
            valid_file_found = False

            # Recursively search all files under the unzipped path
            for root, _, files in os.walk(unzipped_path):
                for file in files:
                    ext = file.split(".")[-1].lower()
                    if ext in desired_extensions:
                        extracted_file = os.path.join(root, file)
                        final_file = os.path.join(target_folder, f"{prod.slug}.{ext}")

                        # Move the valid file to the target folder
                        shutil.move(extracted_file, final_file)
                        prod.files.append(f"{prod.slug}.{ext}")

                        valid_file_found = True
                        break

                if valid_file_found:
                    break

            if not valid_file_found:
                logger.write(
                    "[WARN]:",
                    f"No valid files with extensions {desired_extensions} found.",
                )
                shutil.rmtree(target_folder)
                return 1

            # Clean up unzipped files and original archive
            shutil.rmtree(unzipped_path)
            if CLEANZIP:
                os.remove(filepath)
        else:
            prod.files.append(f"{prod.slug}.{suffix}")

        # Handle screenshots
        if prod.screenshots and prod.screenshots[0] != "None":
            print(prod.screenshots)
            try:
                r = requests.get(
                    prod.screenshots[0], allow_redirects=True, timeout=None
                )
                screen_ext = prod.screenshots[0].split(".")[-1].lower()
                screen_file = os.path.join(target_folder, f"{prod.slug}.{screen_ext}")
                with open(screen_file, "wb") as f:
                    f.write(r.content)

                # Convert to PNG if necessary
                if screen_ext != "png":
                    img = Image.open(screen_file).convert("RGB")
                    png_file = os.path.join(target_folder, f"{prod.slug}.png")
                    img.save(png_file, "PNG")
                    os.remove(screen_file)
                    prod.screenshots[0] = f"{prod.slug}.png"
                else:
                    prod.screenshots[0] = f"{prod.slug}.png"
            except Exception as e:
                logger.write(
                    "[ERR]:", f"Failed to download screenshot for {prod.slug}: {e}"
                )
                prod.screenshots = []

    else:
        logger.write(
            "[WARN]:", f"Directory already exists for {prod.slug}. Skipping..."
        )
        return 1
    return 0


def fix_extentions(desired_extentions):
    """
    given a theorical list of extensions, it returns a list containing additional correct extensions (like CGB, AGB)
    in this way, we deals with these kind of files
    """
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
    """
    build the json file contained in each directory
    """
    if os.path.exists(entrypath + prod.slug):
        jsondata = {
            "developer": prod.developer,
            "description": prod.description if prod.description != "" else "",
            "files": [
                {
                    "default": True,
                    "filename": prod.files[0] if len(prod.files) != 0 else [],
                    "playable": True,
                }
            ],
            "platform": prod.platform,
            "screenshots": [screen for screen in prod.screenshots]
            if len(prod.screenshots) != 0
            else [],
            "slug": prod.slug,
            "title": prod.title,
            "website": [prod.url2],
            "date": prod.date,
        }

        # adding optional fields
        if len(prod.typetag) != 0:
            jsondata["typetag"] = prod.typetag

        if prod.repository != "":
            jsondata["repository"] = prod.repository

        updateJSON(jsondata, entrypath + prod.slug + "/game.json")
    else:
        logger.write(
            "[ERR]",
            "Unable to create file for "
            + prod.slug
            + ". There is no directory for this prod.",
        )
        return 1
    return 0


def updateJSON(data, path):
    jsonstr = json.dumps(data, sort_keys=True, indent=4)
    jsonfile = open(path, "w")
    jsonfile.write(jsonstr)
    jsonfile.close()
