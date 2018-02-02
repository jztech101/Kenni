#!/usr/bin/env python
# coding=utf-8
"""
ip.py - kenni IP Lookup Module
Copyright 2013, Michael Yanovich (yanovich.net)
Copyright 2011, Dimitri Molenaars (TyRope.nl)
Licensed under the Eiffel Forum License 2.

More info:
 * Willie: http://willie.dftba.net
* jenni: https://github.com/myano/jenni/ * Phenny: http://inamidst.com/phenny/

This module has been imported from Willie.
"""


import json
import re
import socket
import web

base = 'http://freegeoip.net/json/'
re_ip = re.compile('(?i)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
re_country = re.compile('(?i)(.+), (.+ of)')

def ip_lookup(kenni, input):
    txt = input.group(2)
    if not txt:
        return kenni.reply("No search term!")
    txt = uc.encode(txt)
    query = uc.decode(txt)
    response = "[IP/Host Lookup] "
    try:
        page = web.get(base + txt)
    except IOError as err:
        return kenni.say('Could not access given address. (Detailed error: %s)' % (err))
    try:
        results = json.loads(page)
    except:
        return kenni.reply('Did not receive proper JSON from %s' % (base))
    if results:
        if re_ip.findall(query):
            ## IP Address
            try:
                hostname = socket.gethostbyaddr(query)[0]
            except:
                hostname = 'Unknown Host'
            response += 'Hostname: ' + str(hostname)
        else:
            ## Host name
            response += 'IP: ' + results['ip']
        spacing = ' |'
        for param in results:
            if not results[param]:
                results[param] = 'N/A'
        if 'city' in results:
            response += '%s City: %s' % (spacing, results['city'])
        if 'region_name' in results:
            response += '%s State: %s' % (spacing, results['region_name'])
        if 'country_name' in results:
            country = results['country_name']
            match = re_country.match(country)
            if match:
                country = ' '.join(reversed(match.groups()))
            response += '%s Country: %s' % (spacing, country)
        if 'zipcode' in results:
            response += '%s ZIP: %s' % (spacing, results['zipcode'])
        response += '%s Latitude: %s' % (spacing, results['latitude'])
        response += '%s Longitude: %s' % (spacing, results['longitude'])
    kenni.reply(response)
ip_lookup.commands = ['ip', 'iplookup', 'host']
ip_lookup.example = ".iplookup 8.8.8.8"

if __name__ == '__main__':
    print(__doc__.strip())
