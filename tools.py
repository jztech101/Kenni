#!/usr/bin/env python2
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

def isChan(chan, checkprefix):
    if not chan:
        return False
    elif chan.startswith("#"):
        return True
    elif checkprefix and len(chan) >= 2 and not chan[0].isalnum() and chan[1] == "#":
        return True
    else:
        return False

