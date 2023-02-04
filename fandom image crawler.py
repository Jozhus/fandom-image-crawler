import urllib.request, os, sys
from bs4 import BeautifulSoup as bs

# Replace with your own stuff
base = "https://maplestory.fandom.com"
outputDir = "./Pictures/Fandom/Maplestory"

seen = set()

def getPage(url):
    return bs(urllib.request.urlopen(url).read().decode("utf-8"), "html.parser")

def getLinks(html):
    return [(x.text, x.get("href")) for x in html.find_all(class_="category-page__member-link")]

def getTitle(html):
    return cleanText(html.find(class_="page-header__title").text)

def getSubtitle(html):
    subtitle = html.find(class_="page-header__page-subtitle")

    if subtitle != None:
        subtitle = cleanText(subtitle.text)
    return subtitle

def getGalleryItems(html):
    return [(x.find("img").get("data-image-name"), x.find("img").get("src").split("/revision")[0]) for x in html.find_all(class_="wikia-gallery-item")]

def getProfileItems(html):
    return [(x.find("img").get("data-image-name"), x.find("img").get("src").split("/revision")[0]) for x in html.find_all(class_="wds-tab__content")]

def cleanText(txt):
    return txt.replace('\t', '').replace('\n', '').replace('\r', '')

def downloadImages(html, title):
    for (imageName, imageSrc) in getProfileItems(html) + getGalleryItems(html):
        filePath = outputDir + '/' + title + '/'
        if not os.path.exists(filePath):
            os.makedirs(filePath)
        if (imageName != None and not os.path.isfile(filePath + imageName)):
            print("      + " + imageName)
            urllib.request.urlretrieve(imageSrc, filePath + imageName)

def crawl(url):
    currPage = getPage(url)
    title = getTitle(currPage)
    subtitle = getSubtitle(currPage)
    seen.add(title)

    if (subtitle != None and subtitle.lower() == "category page"):
        print('[' + title + ']')
        for (linkTitle, linkUrl) in getLinks(currPage):
            if (linkTitle not in seen):
                crawl(base + linkUrl) 
    else:
        print("   > " + title)
        downloadImages(currPage, title)
        return

if __name__ == "__main__":
   crawl(sys.argv[1])
