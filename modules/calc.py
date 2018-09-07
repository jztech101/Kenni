#!/usr/bin/env python3
#coding=utf-8

import html.parser
import json
import re
import string
import urllib.request, urllib.parse, urllib.error
import web
from modules import unicode as uc

c_pattern = r'(?ims)<(?:h2 class="r"|div id="aoba")[^>]*>(.*?)</(?:h2|div)>'
c_answer = re.compile(c_pattern)
r_tag = re.compile(r'<(?!!)[^>]+>')
WAKEY_NOTFOUND = "Please sign up for WolframAlpha's API to use this function. http://products.wolframalpha.com/api/"


def math(kenni, input):
    if not input.group(2):
        return kenni.say("No search term.")

    txt = input.group(2)
    txt = txt.encode('utf-8')
    txt = txt.decode('utf-8')
    txt = urllib.parse.quote(txt.replace('+', '%2B'))

    url = 'http://gamma.sympy.org/input/?i='

    re_answer = re.compile(r'<script type="\S+; mode=display".*?>(.*?)</script>')

    page = web.get(url + txt)

    results = re_answer.findall(page.decode('utf-8'))

    if results:
        kenni.say(results[0])
    else:
        kenni.say('No results found on gamma.sympy.org!')
math.commands = ['math']


def get_wa(search, appid):
    txt = search
    txt = txt.decode('utf-8')
    txt = txt.encode('utf-8')
    txt = urllib.parse.quote(txt)

    uri = 'https://api.wolframalpha.com/v2/query?reinterpret=true&appid=' + appid
    uri += '&input=' + txt

    page = web.get(uri)

    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return "Please install 'bs4', also known as BeautifulSoup via pip to use WolframAlpha."

    soup = BeautifulSoup(page, 'html.parser')
    attempt_one = soup.find_all(attrs={'primary':'true'})

    answer = 'No answers found!'

    if attempt_one:
        answer = attempt_one[0].plaintext.get_text()
        if not answer:
            answer = attempt_one[0].imagesource.get_text()
    else:
        for pod in soup.find_all('pod'):
            if pod.get('title') != 'Input interpretation' and pod.plaintext.get_text():
                answer = pod.plaintext.get_text()
                break

    return answer


def wa(kenni, input):
    if not hasattr(kenni.config, 'wolframalpha_apikey'):
        return kenni.say(WAKEY_NOTFOUND)

    appid = kenni.config.wolframalpha_apikey

    if not input.group(2):
        return kenni.say("No search term.")

    txt = input.group(2)
    txt = txt.encode('utf-8')
    txt = txt.decode('utf-8')
    txt = txt.encode('utf-8')

    result = get_wa(txt, appid)

    if not result:
        return kenni.say("No results found.")

    return kenni.say(html.unescape(result))
wa.commands = ['wolf','wa', 'calc','convert']

if __name__ == '__main__':
    print(__doc__.strip())
