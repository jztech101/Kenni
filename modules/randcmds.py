#!/usr/bin/env python3# -*- coding: utf-8 -*-
from random import randint
def potato(kenni, input):
    kenni.write(['PRIVMSG', input.sender], '\x01ACTION is a potato\x01')
potato.commands = ['potato']
potato.priority = 'high'
def moo(kenni, input):
    kenni.say('MoooooOoooOooooooooooo')
moo.commands = ['moo']
moo.priority = 'high'
def cookie(kenni, input):
    nick = input.nick
    if input.group(2):
        nick = input.group(2)
    kenni.write(['PRIVMSG', input.sender], '\x01ACTION gives ' + nick + ' a cookie\x01')
cookie.commands = ['cookie']
cookie.priority = 'high'
def source(kenni, input):
    kenni.say('Kenni: https://github.com/jztech101/kenni')
source.commands = ['source']
source.priority = 'high'
def shrug(kenni, input):
    kenni.say('┻━┻ ︵ ¯\_(ツ)_/¯ ︵ ┻━┻')
shrug.commands = ['shrug']
shrug.priority = 'high'
def snake(kenni, input):
    msg = "\x01ACTION 's snake slithers by and wraps around " + input.nick + " whispering \"oooo dinnner\"\x01"
    if input.group(2):
        msg = input.nick + "\'s snake slithers by and wraps around " + input.group(2) + " whispering \"oooo dinnner\""
    kenni.write(['PRIVMSG', input.sender], msg)
snake.commands = ['snake']
snake.priority = 'high'
def hmmm(kenni, input):
#    kenni.say('t' + u'\u200b' + 'est')
    kenni.say(kenni.hostmasks["JZTech101"])
hmmm.commands = ['hmmm']
hmmm.priority = 'high'
def coin(kenni, input):
    x = randint(1,100)
    if x > 50:
        kenni.say("heads")
    else:
        kenni.say("tails")
coin.commands = ['coin', 'flip']
coin.priority = 'high'
if __name__ == '__main__':
    print(__doc__.strip())
