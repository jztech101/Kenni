#!/usr/bin/env python3# coding=utf-8
import json
import re
import socket
import web
from modules import unicode as uc


base = 'http://ip-api.com/json/'
re_ip = re.compile('(?i)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
re_country = re.compile('(?i)(.+), (.+ of)')

def ip_lookup(kenni, input):
    txt = input.group(2)
    if not txt:
        return kenni.say("No search term!")
    response = "[IP/Host Lookup] "
    try:
        page = web.get(base + txt)
    except IOError as err:
        return kenni.say('Could not access given address. (Detailed error: %s)' % (err))
    try:
        results = json.loads(page.decode('utf-8'))
    except:
        return kenni.say('Did not receive proper JSON from %s' % (base))
    if results:
        response += txt
        spacing = ' |'
        for param in results:
            if not results[param]:
                results[param] = 'N/A'
        if 'query' in results:
            response += '%s Query: %s' %(spacing, results['query'])
        if 'city' in results:
            response += '%s City: %s' % (spacing, results['city'])
        if 'regionName' in results:
            response += '%s State: %s' % (spacing, results['regionName'])
        if 'country' in results:
            country = results['country']
            match = re_country.match(country)
            if match:
                country = ' '.join(reversed(match.groups()))
            response += '%s Country: %s' % (spacing, country)
        if 'timezone' in results:
            response += '%s Time Zone: %s' % (spacing, results['timezone'])
        if 'as' in results:
            response += '%s AS: %s' % (spacing, results['as'])
        if  'isp' in results:
            response += '%s ISP: %s' % (spacing, results['isp'])
    kenni.say(response)
ip_lookup.commands = ['ip','geoip', 'iplookup']
ip_lookup.example = ".iplookup 8.8.8.8"

if __name__ == '__main__':
    print(__doc__.strip())
