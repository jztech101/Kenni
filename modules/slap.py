#!/usr/bin/env python2

import random
import tools


def slap(kenni, input):
    """.slap <target> - Slaps <target>"""
    text = input.group().split()
    if len(text) < 2 or tools.isChan(text[1], False): return
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
