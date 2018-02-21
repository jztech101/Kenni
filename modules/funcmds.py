#!/usr/bin/env python3# -*- coding: utf-8 -*-
import random
import tools
def roulette(kenni, input):
    if not tools.isChan(input.sender, False):
        return
    random.seed()
    randnum = random.randint(1,3)
    if randnum == 2:
        if kenni.nick in kenni.ops[input.sender]:
            kenni.write(['KICK', input.sender, input.nick, "BANG"])
        else:
            kenni.write(['PRIVMSG', input.sender], "\x01ACTION kicks " + input.nick +"\x01")
    else:
        kenni.say("*CLICK*")
roulette.commands = ['roulette']
roulette.priority= 'high'

if __name__ == '__main__':
    print(__doc__.strip())
