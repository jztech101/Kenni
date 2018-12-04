#!/usr/bin/env python3
import re
import web
import html.parser
import requests
import random
from bs4 import BeautifulSoup
def stripHTML(input):
    pass1 = re.compile("(?s)<[^>]*>(\\s*<[^>]*>)*")
    pass2 = re.compile("&.*?;")
    pass3 = re.compile("<.*?>")
    input = re.sub(pass1, "", input)
    input = re.sub(pass2, "", input)
    input = re.sub(pass3, "", input)
def button(kenni, input):
    eofstring = re.compile(" $")
    space = re.compile(" +")
    begstring = re.compile("^[^A-Za-z0-9]+")
    url = "http://willyoupressthebutton.com"
    page = BeautifulSoup(web.get(url), 'html.parser')
    reward = page.find("div", id="cond")
    reward = re.sub(space," ",reward.text.replace(".","").lower())
    reward = re.sub(begstring,"",reward)
    but = page.find("div", id="res")
    but = re.sub(space, " ", but.text.replace(".","").lower())
    but = re.sub(eofstring,"",but)
    kenni.say("The button reads \"" + reward.capitalize() + "BUT" + but + "\", will you push the button?")
button.commands = ['button']

if __name__ == '__main__':
    print(__doc__.strip())
