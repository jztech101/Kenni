#!/usr/bin/env python2
import random


def interjection(kenni, input):
    """response to interjections"""
    kenni.say(input.nick + '!')
interjection.rule = r'($nickname!)'
interjection.priority = 'high'
interjection.example = '$nickname!'

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

