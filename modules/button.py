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
    url = "http://willyoupressthebutton.com"
    page = BeautifulSoup(web.get(url), 'html.parser')
    reward = page.find("div", id="cond")
    but = page.find("div", id="res")
    kenni.say("The button reads" + reward.text.replace("  "," ").replace("  "," ").lower() + "BUT" + but.text.replace("  "," ").replace("  ", " ").lower() + ", will you push the button?")
button.commands = ['button']

if __name__ == '__main__':
    print(__doc__.strip())
