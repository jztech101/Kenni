#!/usr/bin/env python
"""
seen.py - kenni Seen Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Copyright 2008-2013, Sean B. Palmer (inamidst.com)
Licensed under the Eiffel Forum License 2.

More info:
* Kenni: https://github.com/JZTech101/Kenni
* jenni: https://github.com/myano/jenni/ 
* Phenny: http://inamidst.com/phenny/
"""

import time

## TODO: Make it save .db to disk

def f_seen(kenni, input):
    """.seen <nick> - Reports when <nick> was last seen."""

    if not input.group(2):
        return kenni.say('Please provide a nick.')
    nick = input.group(2).lower()

    if not hasattr(kenni, 'seen'):
        return kenni.reply('?')

    if kenni.seen.has_key(nick):
        channel, t = kenni.seen[nick]
        t = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(t))
        msg = 'I last saw %s at %s in some channel.' % (nick, t)
        kenni.say(msg)
    else:
        kenni.say("Sorry, I haven't seen %s around." % nick)
f_seen.rule = r'(?i)^\+(seen)\s+(\w+)'
f_seen.rate = 15

def f_note(kenni, input):
    try:
        if not hasattr(kenni, 'seen'):
            kenni.seen = dict()
        if input.sender.startswith('#'):
            kenni.seen[input.nick.lower()] = (input.sender, time.time())
    except Exception, e: print e
f_note.rule = r'(.*)'
f_note.priority = 'low'

if __name__ == '__main__':
    print __doc__.strip()
