#!/usr/bin/env python3
from datetime import datetime
from subprocess import *
import sys


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
    print(__doc__.strip())
