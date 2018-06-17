#!/usr/bin/env python3
import re
import web
import html.parser
import requests
from bs4 import BeautifulSoup
def colorize(text):
    return '\x02\x0303' + text + '\x03\x02'
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
            x = len(results)
            if(x > 3):
                x = 3
            msg = None
            for y in range(x):
                title = results[y].find("div",class_="resultTitlePane").find("a",class_="resultTitle").text
                url = results[y].find("div",class_="resultDisplayUrlPane").find("a",class_="resultDisplayUrl").text
                if not msg:
                    msg = colorize(title) + " (" + url + ")"
                else:
                    msg += colorize(title) + " (" + url + ")"
                if y != x-1:
                    msg += " - "
            kenni.say(msg)
search.commands = ['yahoo', 'dogpile', 'search']

def google(kenni, input):
    query = input.group(2)
    if not query:
        kenni.say("Please enter a query")
    else:
        url = "https://www.google.com/search?safe=strict&query=" + query.replace(" ","%20")
        page = BeautifulSoup(requests.get(url).text, 'html.parser')
        results = page.find_all("div", class_="g")
        if(len(results) <1):
            kenni.say("No results found")
            return
        else:
            x = len (results)
            if (x > 3):
                x = 3
            msg = None
            for y in range(x):
                continues = False
                while (not results[y].find("h3",class_="r") or not results[y].find("h3",class_="r").find("a") or not results[y].find("cite")):
                    if y == x and len(results) >= y+1:
                        y += 1
                    elif len(results) >= x+1:
                        y=x+1
                    else:
                        continues = True
                        break
                if continues:
                    continue
                title = results[y].find("h3",class_="r").find("a").text
                url = results[y].find("cite").text
                if not msg:
                    msg = colorize(title) + " (" + url + ")"
                else:
                    msg += colorize(title) + " (" + url + ")"
                if y != x-1:
                    msg += " - "
            if len(msg) > 300:
                msg = msg[:295]+"[...]"
            kenni.say(msg)
google.commands = ['google']
if __name__ == '__main__':
    print(__doc__.strip())
