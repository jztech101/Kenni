#!/usr/bin/env python3
import re
import web
import html.parser
import requests
import random
import tools
from bs4 import BeautifulSoup
def quote(kenni, input):
    regex = re.compile('<.*?>|&.*;')
    topics = ['love','life','inspirational','humor','philosophy','truth','religion','wisdom','inspiration','happiness','romance','hope','death','poetry','faith','writing','success','knowledge','relationships','education','motivation','life-lessons','time','science','funny','books','spirituality']
    topic = random.choice(topics)
    url = "https://www.goodreads.com/quotes/tag/" + topic + "?page=" + str(random.randint(1,101))
    page = BeautifulSoup(web.get(url), 'html.parser')
    results = page.find_all("div",class_= "quote")
    quote = random.choice(results).find("div",class_="quoteText")
    quote = "["+ topic.capitalize() + "] " + re.sub(regex, '', quote.text).replace("\n"," ").replace("  "," ").replace("  "," ").split("//")[0]
    splitquote = quote.split("―")
    if len(quote) > tools.charlimit:
        quote = splitquote[0][:tools.charlimit-5] + "[...] ― " +  splitquote[1]
    kenni.say(quote)
quote.commands = ['quote']

if __name__ == '__main__':
    print(__doc__.strip())
