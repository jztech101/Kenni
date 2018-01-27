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

if __name__ == '__main__':
    print __doc__.strip()

