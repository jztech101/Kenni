#!/usr/bin/env python
"""
roulette.py - kenni Roulette Game Module
Copyright 2010-2013, Kenneth Sham
Licensed under the Eiffel Forum License 2.

More info:
* jenni: https://github.com/myano/jenni/ * Phenny: http://inamidst.com/phenny/
"""

import random
from datetime import datetime, timedelta
random.seed()

# edit this setting for roulette counter. Larger, the number, the harder the game.
ROULETTE_SETTINGS = {
    # the bigger the MAX_RANGE, the harder/longer the game will be
    'MAX_RANGE' : 5,

    # game timeout in minutes (default is 1 minute)
    'INACTIVE_TIMEOUT' : 1,
}

# edit this setting for text displays
ROULETTE_STRINGS = {
    'TICK' : '*TICK*',
    'KICK_REASON' : '*SNIPED! YOU LOSE!*',
    'GAME_END' : 'Game stopped.',
    'GAME_END_FAIL' : "%s: Please wait %s seconds to stop Roulette.",
}

## do not edit below this line unless you know what you're doing
ROULETTE_TMP = {
    'LAST-PLAYER' : None,
    'NUMBER' : None,
    'TIMEOUT' :timedelta(minutes=ROULETTE_SETTINGS['INACTIVE_TIMEOUT']),
    'LAST-ACTIVITY' : None,
}

def roulette (kenni, input):
    global ROULETTE_SETTINGS, ROULETTE_STRINGS, ROULETTE_TMP
    if ROULETTE_TMP['NUMBER'] is None:
        ROULETTE_TMP['NUMBER'] = random.randint(0,ROULETTE_SETTINGS['MAX_RANGE'])
        ROULETTE_TMP['LAST-PLAYER'] = input.nick
        ROULETTE_TMP['LAST-ACTIVITY'] = datetime.now()
        kenni.reply(ROULETTE_STRINGS['TICK'])
        return
    if ROULETTE_TMP['LAST-PLAYER'] == input.nick:
        return
    ROULETTE_TMP['LAST-ACTIVITY'] = datetime.now()
    ROULETTE_TMP['LAST-PLAYER'] = input.nick
    if ROULETTE_TMP['NUMBER'] == random.randint(0,ROULETTE_SETTINGS['MAX_RANGE']):
        kenni.write(['KICK', '%s %s :%s' % (input.sender, input.nick, ROULETTE_STRINGS['KICK_REASON'])])
        ROULETTE_TMP['LAST-PLAYER'] = None
        ROULETTE_TMP['NUMBER'] = None
        ROULETTE_TMP['LAST-ACTIVITY'] = None
    else:
        kenni.reply(ROULETTE_STRINGS['TICK'])
roulette.commands = ['roulette']
roulette.priority = 'low'
roulette.rate = 60

def rouletteStop (kenni, input):
    global ROULETTE_TMP, ROULETTE_STRINGS
    if ROULETTE_TMP['LAST-PLAYER'] is None:
        return
    if datetime.now() - ROULETTE_TMP['LAST-ACTIVITY'] > ROULETTE_TMP['TIMEOUT']:
        kenni.reply(ROULETTE_STRINGS['GAME_END'])
        ROULETTE_TMP['LAST-ACTIVITY'] = None
        ROULETTE_TMP['LAST-PLAYER'] = None
        ROULETTE_TMP['NUMBER'] = None
    else:
        kenni.reply(ROULETTE_STRINGS['GAME_END_FAIL'] % (input.nick, ROULETTE_TMP['TIMEOUT'].seconds - (datetime.now() - ROULETTE_TMP['LAST-ACTIVITY']).seconds))
rouletteStop.commands = ['roulette-stop']
roulette.priority = 'low'
roulette.rate = 60

if __name__ == '__main__':
    print(__doc__.strip())
