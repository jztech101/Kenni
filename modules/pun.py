#!/usr/bin/env python
"""
pun.py - kenni Pun Module
Copyright 2009-2015, Michael Yanovich (yanovich.net)
Copyright 2008-2015, Sean B. Palmer (inamidst.com)
Copyright 2015, Jonathan Arnett (j3rn.com)

More info:
* Kenni: https://github.com/JZTech101/Kenni
* jenni: https://github.com/myano/jenni/ 
* Phenny: http://inamidst.com/phenny/
"""

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
