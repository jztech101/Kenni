#!/usr/bin/env python2

import re
import web


def puns(kenni, input):
    url = 'http://www.punoftheday.com/cgi-bin/randompun.pl'
    exp = re.compile(r'<div class="dropshadow1">\n<p>(.*?)</p>\n</div>')
    page = web.get(url)

    result = exp.search(page)
    if result:
        pun = result.groups()[0]
        return kenni.say(pun)
    else:
        return kenni.say("I'm afraid I'm not feeling punny today!")
puns.commands = ['puns', 'pun', 'badpun', 'badpuns']

if __name__ == '__main__':
    print __doc__.strip()
