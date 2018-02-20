#!/usr/bin/env python3
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
    print(__doc__.strip())

