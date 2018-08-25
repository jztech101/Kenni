#!/usr/bin/env python3
import re
import web
import html.parser
import requests
import tools
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
            msg = None
            y=0
            while not msg or len(msg) < tools.charlimit-20:
                title = results[y].find("div",class_="resultTitlePane").find("a",class_="resultTitle").text
                url = results[y].find("div",class_="resultDisplayUrlPane").find("a",class_="resultDisplayUrl").text
                if not msg:
                    msg = colorize(title) + " [ " + url + " ]"
                else:
                    msg += " - " + colorize(title) + " [ "+url+" ]"
                y+=1
            if len(msg) > tools.charlimit:
                msg = msg[:tools.charlimit-5]+"[...]"
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
            msg = None
            y=0
            while not msg or len(msg) < tools.charlimit-20:
                continues = False
                while (not results[y].find("h3",class_="r") or not results[y].find("h3",class_="r").find("a") or not results[y].find("cite")):
                    if len(results) >= y+1:
                        y += 1
                    else:
                        continues = True
                        break
                if continues:
                    continue
                title = results[y].find("h3",class_="r").find("a").text
                url = results[y].find("cite").text.replace(" ","")
                if not msg:
                    msg = colorize(title) + " [ " + url + " ]"
                else:
                    msg += " - " + colorize(title) + " [ " + url + " ]"
                y+=1
            if len(msg) > tools.charlimit:
                msg = msg[:tools.charlimit-5]+"[...]"
            kenni.say(msg)
google.commands = ['google']
if __name__ == '__main__':
    print(__doc__.strip())
