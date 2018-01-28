#!/usr/bin/env python
# -*- coding: utf-8 -*-

def potato(jenni, input):
    jenni.write(['PRIVMSG', input.sender], '\x01ACTION is a potato\x01')
potato.commands = ['potato']
potato.priority = 'high'
def moo(jenni, input):
    jenni.reply('mooooooooooo')
moo.commands = ['moo']
moo.priority = 'high'
def cookie(jenni, input):
    nick = input.nick
    if input.group(2):
        nick = input.group(2)
    jenni.write(['PRIVMSG', input.sender], '\x01ACTION gives ' + nick + ' a cookie\x01')
cookie.commands = ['cookie']
cookie.priority = 'high'
def source(jenni, input):
    jenni.reply('https://github.com/jztech101/jenni')
source.commands = ['source']
source.priority = 'high'
def shrug(jenni, input):
    jenni.reply('┻━┻ ︵ ¯\_(ツ)_/¯ ︵ ┻━┻')
shrug.commands = ['shrug']
shrug.priority = 'high'
if __name__ == '__main__':
    print __doc__.strip()
