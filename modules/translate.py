#!/usr/bin/env python3# coding=utf-8
import json
import re
import socket
import web
from modules import unicode as uc


def translate(kenni, input):
    base = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key='
    if not hasattr(kenni.config, 'yandex_apikey'):
        return kenni.say('Please sign up for a Yandex API key')
    else:
        base = base + kenni.config.yandex_apikey + "&lang=en&text="
    txt = input.group(2)
    if not txt:
        return kenni.say("No search term!")
    response = "["
    try:
        page = web.get(base + txt.replace(" ","%20"))
    except IOError as err:
        return kenni.say('Could not access given address. (Detailed error: %s)' % (err))
    try:
        results = json.loads(page.decode('utf-8'))
    except:
        return kenni.say('Did not receive proper JSON from %s' % (base))
    if results:
        if results['code'] == 200:
            kenni.say(response + results['lang'] + "] " + " ".join(results['text']))
        else:
            kenni.say("No translation found")
translate.commands = ['tr', 'translate']
translate.example = ".iplookup 8.8.8.8"

if __name__ == '__main__':
    print(__doc__.strip())
