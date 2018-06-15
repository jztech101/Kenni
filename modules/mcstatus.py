#!/usr/bin/env python3# coding=utf-8
import json
import re
import socket
import web
from modules import unicode as uc


base = 'https://status.mojang.com/check'
def mcstatus(kenni, input):
    response = "[MC Status] "
    try:
        page = web.get(base)
    except IOError as err:
        return kenni.say('Could not access given address. (Detailed error: %s)' % (err))
    try:
        results = json.loads(page.decode('utf-8'))
    except:
        return kenni.say('Did not receive proper JSON from %s' % (base))
    if results:
        websitemc = "Minecraft.net: " + getstatus(results[0]['minecraft.net'])
        api = "API: " + getstatus(results[5]['api.mojang.com'])
        account = "Account: " + getstatus(results[2]['account.mojang.com'])
        session = "Session: " + getstatus(results[1]['session.minecraft.net'])
        sessionserver = "Session Server: " + getstatus(results[4]['sessionserver.mojang.com'])
        auth = "Auth Server: " + getstatus(results[3]['authserver.mojang.com'])
        textures = "Textures: " + getstatus(results[6]['textures.minecraft.net'])
        website = "Mojang.com: " + getstatus(results[7]['mojang.com'])
        response = website + " - " + websitemc + " - " + account + " - " + auth + " - " + session +" - " + sessionserver + " - " + textures + " - " + api
    kenni.say(response)
def getstatus(input):
    if input == 'green':
        return 'Online'
    elif input == 'yellow':
        return 'Overloaded'
    else:
        return 'Offline'
mcstatus.commands = ['mcstatus']
mcstatus.example = ".iplookup 8.8.8.8"

if __name__ == '__main__':
    print(__doc__.strip())
