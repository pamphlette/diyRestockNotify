# this is specific to HTML from mundiflora.com but can be generalized to others
# currently operates under the assumption that an HTML file exists in scrapes

from bs4 import BeautifulSoup
from notifications import notify
import plantScraper.scrapers.captchaScrape as scrape
import re

# update the wishlist sp from mundi
RESTOCK_SPECIES = [
    'Begonia aff genimiflora',
    'Begonia aff tropaeolifolia',
    'Begonia sp 14',
    'Begonia tropaeolifolia',
    'Begonia sp red'
]

def getItems(soup: BeautifulSoup, tag: str, searchStr: str = None) -> list:
    """
    Returns a soupified list of products from given html based on input tag and
    (optional) regex-assisted search for class name

    :return list:  Soupified versions of every product on the given html
    """
    if searchStr: 
        items = soup.find_all(tag, class_= re.compile(searchStr))
    else: 
        items = soup.find_all(tag)
    
    return items

def getAttributes(items: list,  tag: str, searchStr: str = None, attNum: int = 0) -> list:
    """
    Return a list of attributes for all products from a given product list of
    BeautifulSoup elements, returns None if list is empty/non-existent

    :return list:   list of 0+ strings with attribute values of products 
    """
    #return empty list if given list is empty or N/A
    if items is None or items.count == 0:
        print('Given list is empty or does not exist')
        return None

    attributes = []
    #iterate over given list and pull the given title
    for i in items:
        if searchStr: 
            item = i.find(tag, re.compile(searchStr))
        else: 
            item = i.find(tag)

        attributes.append(item.contents[attNum])

    return attributes

def getSiteSoup(site: str, url: str) -> BeautifulSoup:
    """
    Runs a fresh scrape on a given URL, saves the html as a separate file and 
    returns a soupified version of the contents

    :return BeautifulSoup:  instance of the scraped website
    """

    site = str.lower(site)              #make sure it is lower case
    fileName = site + "Out.html"
    filePath = "scrapes/" + fileName
    soup = BeautifulSoup()
    
    with open(filePath, 'w', encoding="utf-8") as file:

        html = scrape.getHTMLCaptcha(url)
        file.write(html)                # write resutlting html to storage file
        contents = html                 # update contents variable

    #read the file to make the soup
    soup = BeautifulSoup(contents, "html5lib")

    return soup

def getfileSoup(site: str) -> BeautifulSoup:
    """
    Searches for a file for the given string with "Out.html" appended to it,
    and returns soupified version of the contents, or none if there is no file

    :return BeautifulSoup:  instance of the scraped store
    """
    site = str.lower(site)              #make sure it is lower case

    try:
        with open("scrapes/" + site + "Out.html", 'r', encoding="utf-8") as file:
            contents = file.read()
            return BeautifulSoup(contents, "html5lib")
    except:
        raise FileNotFoundError("No such file exists or another error occured")

if __name__ == "__main__":

    # get a soup to work with (either from url or file)
    soup = getfileSoup("mundiflora")

    # get a list of all soup items to explore further
    products = getItems(soup, 'li', 'type-product')

    # make output data and get ready to fill it
    species = getAttributes(products, 'h2', 'title' )
    prices = getAttributes(products, 'bdi', attNum = 1)
    mundiData = dict().fromkeys(species)

    # fill output dict for Mundiflora
    for i in range(len(species)):
        # check to see if the attribute has a value related to stock
        stockCheck = products[i].attrs['class'][4]
        #if that value is stock-related, keep it, if not re-asign it to [5]
        if 'stock' not in stockCheck:
            stockCheck = products[i].attrs['class'][5]

        # add an item from each index to make a nested array for each species
        mundiData[species[i]] = [prices[i], stockCheck]

    # iterate over the array to check stock of items
    for x in RESTOCK_SPECIES:
        availability = mundiData.get(x)[1]
        print(str(x) + " - " + availability)
        if 'instock' in availability:
            notify.notification(str(x) + " is back in stock!")

    #TODO: 
        # Modify the scraper function to just run each time 
        # Set a sleep times and upload to pi
        # save things in a more digestible way
