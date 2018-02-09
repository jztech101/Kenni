#!/usr/bin/env python
"""
tools.py - kenni Tools
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Copyright 2008-2013, Sean B. Palmer (inamidst.com)
Licensed under the Eiffel Forum License 2.

More info:
* Kenni: https://github.com/JZTech101/Kenni
* jenni: https://github.com/myano/jenni/ 
* Phenny: http://inamidst.com/phenny/
"""

def deprecated(old):
    def new(kenni, input, old=old):
        self = kenni
        origin = type('Origin', (object,), {
            'sender': input.sender,
            'nick': input.nick
        })()
        match = input.match
        args = [input.bytes, input.sender, '@@']

        old(self, origin, match, args)
    new.__module__ = old.__module__
    new.__name__ = old.__name__
    return new

if __name__ == '__main__':
    print __doc__.strip()

def isChan(chan, checkprefix):
    if chan.startswith("#"):
        return True
    elif checkprefix and not chan[0].isalnum() and chan[1] == "#":
        return True
    else:
        return False

