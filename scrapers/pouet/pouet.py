from Production import Production
import pouet_common
import requests
import unicodedata
import re
import os
from bs4 import BeautifulSoup
from unidecode import unidecode
import zipfile

import shutil
import fnmatch

print("WARNING: if a prod is already present in the gamesList with another slugname, two different entries will be created!")
    
baseurl = "https://pouet.net"

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))

    return result
def build_slug(slug: str):
    # delete characters not needed in the slug
    slug = re.sub("[^0-9a-zA-ZÀ-ÖØ-öø-ÿ]+", " ", slug)  # removes all except letters and numbers
    slug = slug.lower() # to lowercase
    slug = slug.strip().replace(" ", "-") # hypens instead of spaces
    slug = unidecode(slug)  # normalize accented characters

    return slug

'''
    - scrape Pouet's prods page and fetches all links
    - each link will be processed (scraped) and a Production object will be built
    - this object will be used to build JSON, files and folders
'''
def scrape(platform):
    #TODO: change variable in the URL: now it only parse demos page
    page = requests.get(baseurl + "/prodlist.php?type%5B%5D=demo&platform%5B%5D=" + platform + "&page=1")
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
        page = requests.get(baseurl + "/prodlist.php?type%5B%5D=demo&platform%5B%5D=Gameboy&page=" + str(i+1))
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
                            

'''
    given a slug and Pouet production url, it returns an object containing everything useful
    to build a file hierarchy
'''
def scrape_page(slug, url):
    # init variables ( if not, lil' python cries :/ )
    screenshots = []
    files = []
    typetag = ""

    page = requests.get(url)
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

'''
    given a prod "Production" object:
    1. create a proper named folder and build a JSON according to Production data field
    2. fetches all slug and add it to gamesList.json
'''
def build(prod: Production):
    entrypath = "a/"

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
        r = requests.get(prod.url, allow_redirects=True)
        open(filepath + prod.slug + "." + suffix, 'wb').write(r.content)

        # unzip in case of zip
        if prod.url.endswith(".zip"):
            # download and unzip
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
                print("[WARN]: cant rename file")
        
            # cleaning up
            shutil.rmtree(filepath + "unzippedfolder")
            os.remove(filepath + prod.slug + "." + "zip")
        else:
            # it is a proper gb file -> just write the filename in its own structure field
            pass
        
        # update production object file
        prod.files.append(prod.slug + "." + suffix)
        
    else:
        print("[WARNING]: directory already present, skipping " + prod.slug + "...")



def main():
    '''
    THIS IS THE PROPER MAIN

    for platform in pouet_common.PLATFORMS:
        scrape(platform)
    '''
    '''
        TESTING AREA
    url = "https://www.pouet.net/prod.php?which=86234"
    p = scrape_page("hey", url)
    
    '''
    scrape("Gameboy")

main()