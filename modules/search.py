#!/usr/bin/env python3
import re
import web
import html.parser
from bs4 import BeautifulSoup
def search(kenni, input):
    query = input.group(2)
    if not query:
        kenni.say("Please enter a query")
    else:
        url = "http://www.dogpile.com/info.dogpl/search/web?ssm=true&q=" + query.replace(" ","%20") + "&fcoid=1573&fcop=results-main&om_nextpage=True"
        page = BeautifulSoup(web.get(url), 'html.parser')
        results = page.find_all("div",class_= "resultsMainRegion")[1].find_all("div",class_= "searchResult")
        if(len(results) < 1):
            kenni.say("No results found")
            return
        else:
            title = results[0].find("div",class_="resultTitlePane").find("a",class_="resultTitle").text
            url = results[0].find("div",class_="resultDisplayUrlPane").find("a",class_="resultDisplayUrl").text
            content = results[0].find("div",class_="resultDescription").text
            kenni.say("[" + title + "] " + content + " - " + url)
search.commands = ['google', 'yahoo', 'dogpile', 'search']

if __name__ == '__main__':
    print(__doc__.strip())
