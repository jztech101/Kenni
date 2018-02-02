#!/usr/bin/env python
"""
ping.py - kenni Ping Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Copyright 2008-2013, Sean B. Palmer (inamidst.com)

More info:
* jenni: https://github.com/myano/jenni/ * Phenny: http://inamidst.com/phenny/
"""

import random


def interjection(kenni, input):
    """response to interjections"""
    kenni.say(input.nick + '!')
interjection.rule = r'($nickname!)'
interjection.priority = 'high'
interjection.example = '$nickname!'

def f_ping(kenni, input):
    """ping kenni in a channel or pm"""
    kenni.reply('pong')
f_ping.commands = ['ping']
f_ping.priority = 'high'

def f_pong(kenni, input):
    kenni.reply('ping')
f_pong.commands = ['pong']
f_pong.priority = 'high'

if __name__ == '__main__':
    print(__doc__.strip())

