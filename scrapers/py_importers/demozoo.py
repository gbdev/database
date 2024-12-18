# dag7 - 2021

# URL is structured in this way:
# https://demozoo.org/productions/?platform={internal_no_platform}&production_type={internal_prodtype_number}


import requests
from bs4 import BeautifulSoup

from py_common.Logger import Logger
from py_common.Production import Production
import py_common.utils as utils

########################
### GLOBAL VARIABLES ###
########################
globalgameslist = utils.gimme_global_games_list()   # slug in entries folder
logger = Logger(utils.PREFERRED_OUTPUT)     # logger will print in file or on console depending on params in utils.PREFERRED_OUTPUT --> LOG or CONSOLE

baseurl = "https://demozoo.org"
blacklist = [
    #"missing-colors",    # file in a folder...must solve this ASAP
    "pdroms-com-relaunch"   # duplicate file (and it doesn't have devs specified)
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
    # dict containing demozoo's categories,
    # with a mapped "simplified" category according to CONTRIBUTING.MD 
    # "game", "homebrew", "demo" or "hackrom"
##
PLATFORMS = {
    "Gameboy": [38, "GB"],
    "Gameboy Color": [37, "GBC"]
    # "Gameboy Advance":[30, "GBA"]
}

# disable utils.DEBUG flag in prod
# Default: "../../entries
entrypath = "py_common/" + utils.BETA_FOLDER + "/" if utils.DEBUG else "../../entries"

#################
### FUNCTIONS ###
#################
def scrape(platform):
    '''
        scrape Demozoo prods page and fetches all links
        - each link will be processed (scraped) and a Production object will be built
        - this object will be used to build JSON, files and folders
    ''' 
    logger.write("[INFO]", "Scraping platform " + platform)
    page = requests.get(baseurl + "/productions/?platform=" + str(PLATFORMS[platform][0]) + "&page=1", timeout=None)
    soup = BeautifulSoup(page.content, 'html.parser')

    # parsing every page
    enough_page = True
    i = 0
    while enough_page:
        if soup.find('a', {"title": "Next_page"}):
            enough_page = True
        else:
            enough_page = False

        logger.write("[INFO]", "Parsing page: " + str(i+1) )
        #TODO: dont call twice this page, as it is called before
        
        page = requests.get(baseurl + "/productions/?platform=" + str(PLATFORMS[platform][0]) + "&page=" + str(i+1), timeout=None)
        soup = BeautifulSoup(page.content, 'html.parser')

        # get the big prods table
        prodTable = soup.findAll('tbody')[0].findAll('a')

        # get links "worth to parse" (those ones that links to a production page)
        links = [ link for link in prodTable if "productions" in link.get("href") ]

        # get rows; for each rows, get the name of the prod and the internal link
        for link in links:
            demozoo_internal_link = baseurl + "/" + link.get("href")
            
            # building slug: all lowercase, each word separated by hyphen, no special character
            slug = utils.build_slug(link.text)

            if slug not in globalgameslist and slug not in blacklist:
                # scrape demozoo's page: the returned object will be used to build the file hierarchy
                prod = scrape_page(slug, demozoo_internal_link, PLATFORMS[platform][1])
                
                if prod != -1:
                    #DBGPRINT slugprint
                    #print(prod.slug)

                    # check if it could be added to database or not
                    # building files
                    ret = utils.build(prod, entrypath, ["gb", "gbc"])   # TODO: GBA, add GBA to this list
                
                    # make required JSON file
                    if ret != 1:
                        ret = utils.makeJSON(prod, entrypath)
                        
                        # useful to print all added entries (to spot duplicates for example)
                        if utils.DEBUG:
                            added.append(prod.slug)
            else:
                if slug in blacklist:
                    logger.write("[WARN]", " " + slug + " in blacklist.")
                elif slug in globalgameslist:
                    logger.write("[WARN]", " " + slug + " already in entries folder!")

def scrape_page(slug, url, platform):
    '''
        given a slug and demozoo production url, it returns an object containing everything useful
        to build a file hierarchy
    '''
    # init variables
    screenshots = []
    files = []
    typetag = ""

    page = requests.get(url, timeout=None)
    soup = BeautifulSoup(page.content, 'html.parser')

    # getting title
    title = str.strip(soup.find('div', {"class": "production_title focus_title"}).findChildren("h2")[0].text)

    logger.write("[INFO]", " Adding: " + title + " ...")

    # getting developer
    developer = str.strip(soup.find('div', {"class": "production_title focus_title"}).findChildren("h3")[0].findChildren("a")[0].text)
    
    # fetching tag
    list_typetag = soup.find('li', {"class": "signpost"})
    if list_typetag == None:
        typetag = ""
    else:
        typetag = str.strip(list_typetag.text if not isinstance(list_typetag, list) else list_typetag[0].text)


    if "TRO" in typetag.upper() or "DEMO" in typetag.upper():
        typetag = "demo"
    elif "GAME" in typetag.upper():
        typetag = "game"
    elif "MUSIC" in typetag.upper():
        typetag = "music"
    elif "INVITATION" in typetag.upper():
        typetag = "demo"
    else:
        logger.write("[WARN]", " We don't care about this category: " + typetag)
        return -1
    
    # fetching screenshot
    screen_obj = soup.find('a', {"class": "screenshot"})
    if screen_obj is not None:
        screenshot = screen_obj.get("href")
    else:
        screenshot = "None"

    screenshots.append(screenshot)

    # fetching source link (if present)
    source = soup.find(lambda tag: tag.name == "a" and "github" in tag.text.lower())
    source = source.get("href") if source else ""

    # fetching url (if present)
    url = soup.find('ul', {"class": "download_links"})
    if url is not None:
        url = url.findChildren("a")
    else:
        # it doesn't make any sense to have a prod without DL link
        logger.write("[ERR]", " No url available for this production ")
        return -1

    if len(url) == 0:
        logger.write("[ERR]", " No url available for this production ")
        return -1
    elif len(url) == 1:
        url = url[0].get("href")
        if "modermodemet.se" in url:
            logger.write("[ERR]", " modermodemet.se is not available, and no other valid link has been found")
            return -1
    elif len(url) >= 2:
        # because almost always the prod will have the secondary mirror as scene.org or smth like that
        url = url[1].get("href")
        if "scene.org" in url and "view" in url:
            url = url.replace("view", "get")

    # fetching video
    video = soup.find(lambda tag: tag.name == "a" and "youtube" in tag.text.lower())
    video = video.get("href") if video else ""
    
    files = [f"{slug}.{platform.lower()}"]

    return Production(title, slug, developer, platform, typetag, screenshots, files, video, repository=source, url=url)

def main():
    for platform in PLATFORMS.keys():
        logger.write("[INFO]","Parsing platform: " + platform)
        scrape(platform)
    
main()

if utils.DEBUG:
    [ logger.write("[TITLE]", f) for f in added ]

logger.write("[INFO]", "demozoo importer ended!")