import requests
from bs4 import BeautifulSoup

# get all the links of months
def trade_spider():
    url = "http://mlg.ucd.ie/modules/COMP41680/news/index.html"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "lxml")
    for link in soup.findAll('a'):
        href = "http://mlg.ucd.ie/modules/COMP41680/news/" + link.get('href')
        get_single_item(href)

# get all the links of articles
def get_single_item(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "lxml")
    for item_title in soup.findAll('a'):
        #         print (item_title.string)
        title = item_title.get('href')
        if (title and title != "index.html"):
            href_item = "http://mlg.ucd.ie/modules/COMP41680/news/" + title
            print (href_item)
        get_article(href_item)

# get all the content of article
def get_article(article_url):
    source_code = requests.get(article_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "lxml")
    title = (soup.findAll('h2'))[0].string
    if (not title.endswith('.')):
        f = open(title + ".txt",'w')
        for article in soup.findAll('p'):
        #         print (article.string)
            if (article.string):
                f.write(article.string)
            else:
                f.write('\n\n')
        f.close()


trade_spider()
