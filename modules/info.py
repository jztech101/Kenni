#!/usr/bin/env python3
from itertools import zip_longest
import tools

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
    for (name, user), count in kenni.stats.items():
        if name in ignore:
            continue
        if not user:
            continue

        if not tools.isChan(user, False):
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

    comrank = sorted([(b, a) for (a, b) in commands.items()], reverse=True)
    userank = sorted([(b, a) for (a, b) in users.items()], reverse=True)
    charank = sorted([(b, a) for (a, b) in channels.items()], reverse=True)

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
    print(__doc__.strip())
