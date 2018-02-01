#!/usr/bin/env python
"""
info.py - kenni Information Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Copyright 2008-2013, Sean B. Palmer (inamidst.com)
Licensed under the Eiffel Forum License 2.

More info:
* jenni: https://github.com/myano/jenni/ * Phenny: http://inamidst.com/phenny/
"""

from itertools import izip_longest

def fchannels():
    try:
        f = open("nochannels.txt", "r")
    except:
        return False
    lines = f.readlines()[0]
    f.close()
    lines = lines.replace('\n', '')
    return lines.split(',')

def stats(kenni, input):
    """Show information on command usage patterns."""
    if input.sender == '##uno':
        return
    commands = dict()
    users = dict()
    channels = dict()


    ignore = set(['f_note', 'startup', 'message', 'noteuri',
                  'say_it', 'collectlines', 'oh_baby', 'chat',
                  'collect_links', 'bb_collect', 'random_chat'])
    for (name, user), count in kenni.stats.iteritems():
        if name in ignore:
            continue
        if not user:
            continue

        if not user.startswith('#'):
            try:
                users[user] += count
            except KeyError:
                users[user] = count
        else:
            try:
                commands[name] += count
            except KeyError:
                commands[name] = count

            try:
                channels[user] += count
            except KeyError:
                channels[user] = count

    comrank = sorted([(b, a) for (a, b) in commands.iteritems()], reverse=True)
    userank = sorted([(b, a) for (a, b) in users.iteritems()], reverse=True)
    charank = sorted([(b, a) for (a, b) in channels.iteritems()], reverse=True)

    # most heavily used commands
    creply = 'most used commands: '
    for count, command in comrank[:10]:
        creply += '%s (%s), ' % (command, count)
    kenni.say(creply.rstrip(', '))

    # most heavy users
    reply = 'power users: '
    k = 1
    for count, user in userank:
        if ' ' not in user and '.' not in user:
            reply += '%s (%s), ' % (user, count)
            k += 1
            if k > 10:
                break
    kenni.say(reply.rstrip(', '))

    # most heavy channels
    chreply = 'power channels: '
    bchannels = fchannels()
    for count, channel in charank[:3]:
        if bchannels and channel in bchannels:
            continue
        chreply += '%s (%s), ' % (channel, count)
    kenni.say(chreply.rstrip(', '))
stats.commands = ['stats']
stats.priority = 'low'

if __name__ == '__main__':
    print __doc__.strip()
