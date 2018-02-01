#!/usr/bin/env python
"""
scores.py - kenni Slap Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)

More info:
* jenni: https://github.com/myano/jenni/ * Phenny: http://inamidst.com/phenny/
"""

import random

def slap(kenni, input):
    """.slap <target> - Slaps <target>"""
    text = input.group().split()
    if len(text) < 2 or text[1].startswith('#'): return
    if text[1] == kenni.nick:
        if (input.nick not in kenni.config.admins):
            text[1] = input.nick
        else: text[1] = 'herself'
    if text[1] in kenni.config.admins:
        if (input.nick not in kenni.config.admins):
            text[1] = input.nick
    verb = random.choice(('slaps', 'kicks', 'destroys', 'annihilates', 'obliterates', 'drop kicks', 'curb stomps', 'backhands', 'punches', 'roundhouse kicks', 'rusty hooks', 'pwns', 'owns'))
    kenni.write(['PRIVMSG', input.sender, ' :\x01ACTION', verb, text[1], '\x01'])
slap.commands = ['slap', 'slaps']
slap.priority = 'medium'
slap.rate = 60

if __name__ == '__main__':
    print __doc__.strip()
