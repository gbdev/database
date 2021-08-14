from Production import Production
import pouet_common
import requests
import unicodedata
import re
import os
from bs4 import BeautifulSoup
from unidecode import unidecode
import zipfile
import urllib.request as request
from contextlib import closing
import shutil
import fnmatch

# since this error is gonna be prompted many times making everything too verbose
PYTHONWARNINGS="ignore:Unverified HTTPS request"

#TODO: find a way to make this print disappears. Currently there is no solution to this issue.
print("[WARN]: if a prod is already present in the gamesList with another slugname, two different entries will be created!")

baseurl = "https://pouet.net"

# global logger: it will be used to diagnose what's wrong (skipped files, 404 errors...)
logger = open("log.txt", "w+")

# find files matching a path in a folder and its subfolders
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))

    return result

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

def scrape(platform):
    '''
        scrape Pouet's prods page and fetches all links
        - each link will be processed (scraped) and a Production object will be built
        - this object will be used to build JSON, files and folders
    '''
    #TODO: change variable in the URL: now it only parse demos page
    page = requests.get(baseurl + "/prodlist.php?type%5B%5D=demo&platform%5B%5D=" + platform + "&page=1", timeout=1)
    soup = BeautifulSoup(page.content, 'html.parser')

    # get total number of pages
    selpages = soup.find("select", {"name":"page"})
    options = selpages.find_all("option")
    print(options)
    numberofpages = int(options[-1].text)

    # parsing every page
    for i in range(0, numberofpages):
        print("\nParsing page: " + str(i))
        #TODO: dont call twice this page, as it is called before
        page = requests.get(baseurl + "/prodlist.php?type%5B%5D=demo&platform%5B%5D=Gameboy&page=" + str(i+1), timeout=1)
        soup = BeautifulSoup(page.content, 'html.parser')

        # get the big prods table
        prodTable = soup.findAll('table')[1].findAll('tr')
        
        # get rows; for each rows, get the name of the prod and the internal link
        for tr in prodTable:
            tds = tr.find_all('td')
            if(tds):
                for td in tds:
                    spans = td.find_all("span", {"class": "prod"}, recursive=False)
                    for span in spans:
                        if span:
                            a = span.findChildren()[0]
                            pouet_internal_link = baseurl + "/" + a.get("href")
                            
                            # building slug: all lowercase, each word separated by hyphen, no special character
                            slug = build_slug(a.text)
                            
                            # scrape pouet's page: the returned object will be used to build the file hierarchy
                            prod = scrape_page(slug, pouet_internal_link)
                            
                            # defining proper platform --> the default one is GB
                            prod.platform = pouet_common.PLATFORMS[platform]
                            
                            # building files
                            build(prod)
                            
def scrape_page(slug, url):
    '''
        given a slug and Pouet production url, it returns an object containing everything useful
        to build a file hierarchy
    '''
    # init variables ( if not, lil' python cries :/ )
    screenshots = []
    files = []
    typetag = ""

    page = requests.get(url, timeout=1)
    soup = BeautifulSoup(page.content, 'html.parser')

    # get the prod data table
    table = soup.find('table', id="pouetbox_prodmain")
    
    # get rows; for each rows, get the name of the prod and the internal link
    '''    for tr in table:
            print(tr)
    '''
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
        typetag = pouet_common.CATEGORIES[span.text]
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
    
    return Production(title, slug, developer, "GB", typetag, screenshots, files, video, repository=source, url=url)

def build(prod: Production):
    '''
        given a prod "Production" object:
        1. create a proper named folder and build a JSON according to Production data field
        2. fetches all slug and add it to gamesList.json
    '''
    # while testing, change it in something gibberish; it may helps a lot and you are not going to directly merge everything in
    # the main folder.
    entrypath = "a/"

    print("[INFO]: " + prod.title + " - " + prod.url)

    if not os.path.exists(entrypath + prod.slug):
        #############
        # PROD FILE #
        #############
        # make its own folder
        os.mkdir(entrypath + prod.slug, 0o777)

        # figuring out the suffix
        suffix = prod.url.split(".")[-1]

        # building the filepath
        filepath = entrypath + prod.slug + "/"

        # download the file
        # in case of http
        if prod.url.startswith("http"):
            r = requests.get(prod.url, allow_redirects=True, timeout=1, verify=False)
            
            if r.status_code == 404:
                logger.write("[ERR]: 404: " + prod.slug + " - " + prod.url)

                # cleaning in case of error
                shutil.rmtree(entrypath + prod.slug)
                return(1)
            
            open(filepath + prod.slug + "." + suffix, 'wb').write(r.content)
        else:
            with closing(request.urlopen(prod.url)) as r:
                with open(filepath + prod.slug + "." + suffix, 'wb') as f:
                    shutil.copyfileobj(r, f)
        
        # unzip in case of zip
        if prod.url.endswith(".zip"):
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

                # proper renaming and moving the file
                if path != []:
                    os.rename(path[0], filepath + prod.slug + "." + suffix)
                else:
                    logger.write("[WARN]: cant rename file")
            
                # cleaning up unneeded files
                shutil.rmtree(filepath + "unzippedfolder")
                os.remove(filepath + prod.slug + "." + "zip")

                pass
            except zipfile.BadZipFile as e:
                logger.write("[ERR] " + str(e) + " bad zip file")
                shutil.rmtree(entrypath + prod.slug)
                return 1
        else:
            # it is a proper gb file -> just write the filename in its own structure field
            pass
        
        # update production object file
        prod.files.append(prod.slug + "." + suffix)
        
        # download the screenshot
        r = requests.get(prod.screenshots[0], allow_redirects=True, timeout=1)
        open(filepath + prod.slug + "." + "png", 'wb').write(r.content)
    else:
        logger.write("[WARN]: directory already present, skipping " + prod.slug + "...")

def main():
    scrape("Gameboy")

main()