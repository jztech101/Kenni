#!/usr/bin/env python
# -*- coding: utf-8 -*-

def potato(kenni, input):
    kenni.write(['PRIVMSG', input.sender], '\x01ACTION is a potato\x01')
potato.commands = ['potato']
potato.priority = 'high'
def moo(kenni, input):
    kenni.reply('mooooooooooo')
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
    kenni.reply('https://github.com/jztech101/kenni')
source.commands = ['source']
source.priority = 'high'
def shrug(kenni, input):
    kenni.reply('┻━┻ ︵ ¯\_(ツ)_/¯ ︵ ┻━┻')
shrug.commands = ['shrug']
shrug.priority = 'high'
if __name__ == '__main__':
    print(__doc__.strip())
