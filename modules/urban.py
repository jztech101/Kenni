#!/usr/bin/env python3
# coding=utf-8
import json
import re
import socket
import web
from modules import unicode as uc


base = 'http://api.urbandictionary.com/v0/define?term='
regex = re.compile("\n|\r|\t")
def urban(kenni, input):
    txt = input.group(2)
    if not txt:
        return kenni.say("No search term!")
    try:
        page = web.get(base + txt.replace(" ","%20"))
    except IOError as err:
        return kenni.say('Could not access given address. (Detailed error: %s)' % (err))
    try:
        results = json.loads(page.decode('utf-8'))
    except:
        return kenni.say('Did not receive proper JSON from %s' % (base))
    if results and len(results.get("list")) > 0:
        result = results.get("list")
        index = 1
        tmp = getDef(result,index)
        if tmp:
            response = regex.sub(" ",tmp).replace("  "," ")
        else:
            kenni.say("No results found")
            return
        while len(response) < 300:
            index += 1
            tmp = getDef(result, index)
            if tmp:
                response = regex.sub(" ",tmp).replace("  "," ")
            else:
                break
        if len(response)>300:
            response = response[:295]+"[...]"
        kenni.say(response)
    else:
        kenni.say("No results found")
def getDef(results, index):
    if results and len(results) >= index:
        word = results[0].get("word")
        response = word + " -- "
        for x in range(0,index):
            if word.lower() == results[x].get("word").lower():
                definition = results[x].get("definition")
                if x == index-1:
                    response += definition
                else:
                    response += definition + " -- "
        return response
    else:
        return
urban.commands = ['ud','urban']
urban.example = "urban"

if __name__ == '__main__':
    print(__doc__.strip())
