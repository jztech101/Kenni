#!/usr/bin/env python2
"""
version.py - kenni Version Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Copyright 2009-2013, Silas Baronda
Licensed under the Eiffel Forum License 2.

More info:
* Kenni: https://github.com/JZTech101/Kenni
* jenni: https://github.com/myano/jenni/ 
* Phenny: http://inamidst.com/phenny/
"""

from datetime import datetime
from subprocess import *


def git_info():
    p = Popen(['git', 'log', '-n 1'], stdout=PIPE, close_fds=True)

    commit = p.stdout.readline()
    author = p.stdout.readline()
    date = p.stdout.readline()
    return commit, author, date


def version(kenni, input):

    kenni.say("Kenni")
version.commands = ['version']
version.priority = 'medium'
version.rate = 10


if __name__ == '__main__':
    print __doc__.strip()
