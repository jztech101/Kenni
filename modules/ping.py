#!/usr/bin/env python
"""
ping.py - jenni Ping Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Copyright 2008-2013, Sean B. Palmer (inamidst.com)

More info:
 * jenni: https://github.com/myano/jenni/
 * Phenny: http://inamidst.com/phenny/
"""

import random


def interjection(jenni, input):
    """response to interjections"""
    jenni.say(input.nick + '!')
interjection.rule = r'($nickname!)'
interjection.priority = 'high'
interjection.example = '$nickname!'

def f_ping(jenni, input):
    """ping jenni in a channel or pm"""
    jenni.reply('pong')
f_ping.commands = ['ping']
f_ping.priority = 'high'

def f_pong(jenni, input):
    jenni.reply('ping')
f_pong.commands = ['pong']
f_pong.priority = 'high'

def potato(jenni, input):
    jenni.write(['PRIVMSG', input.sender], '\x01ACTION is a potato')
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
if __name__ == '__main__':
    print __doc__.strip()
def source(jenni, input):
    jenni.reply('https://github.com/jztech101/jenni')
source.commands = ['source']
source.priority = 'high'
