#!/usr/bin/env python2
"""
ping.py - kenni Ping Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Copyright 2008-2013, Sean B. Palmer (inamidst.com)

More info:
* Kenni: https://github.com/JZTech101/Kenni
* jenni: https://github.com/myano/jenni/
* Phenny: http://inamidst.com/phenny/
"""

import random

def f_ping(kenni, input):
    """ping kenni in a channel or pm"""
    kenni.say('pong')
f_ping.commands = ['ping']
f_ping.priority = 'high'

def f_pong(kenni, input):
    kenni.say('ping')
f_pong.commands = ['pong']
f_pong.priority = 'high'

if __name__ == '__main__':
    print __doc__.strip()

