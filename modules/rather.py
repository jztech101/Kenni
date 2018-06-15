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
def rather(kenni, input):
    url = "http://either.io/"
    page = BeautifulSoup(web.get(url), 'html.parser')
    result1 = page.find("div", class_="result-1")
    result2 = page.find("div", class_="result-2")
    option1 = result1.find("span", class_="option-text").text.lower() + " (" + result1.find("div", class_="percentage").find("span").text.lower() + "%)"
    option2 = result2.find("span", class_="option-text").text.lower() + " (" + result2.find("div", class_="percentage").find("span").text.lower() + "%)"
    kenni.say("Would you rather " + option1 + " OR " + option2 + "?")
rather.commands = ['rather']

if __name__ == '__main__':
    print(__doc__.strip())
