#!/usr/bin/env python3
 import proxy
import re
import web


def isup(kenni, input):
    '''isup.me website status checker'''
    site = input.group(2)
    if not site:
        return kenni.say('What site do you want to check?')
    if ' ' in site:
        idx = site.find(' ')
        site = site[:idx+1]
    site = (site).strip()

    if site[:7] != 'http://' and site[:8] != 'https://':
        if '://' in site:
            protocol = site.split('://')[0] + '://'
            return kenni.say('Try it again without the %s' % protocol)
        else:
            site = 'http://' + site
    try:
        response = proxy.get(site)
    except Exception as e:
        kenni.say(site + ' looks down from here.')
        return

    if response:
        kenni.say(site + ' looks fine to me.')
    else:
        kenni.say(site + ' is down from here.')
isup.commands = ['isup']
isup.example = '.isup google.com'

if __name__ == '__main__':
    print(__doc__.strip())
