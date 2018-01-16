#!/usr/bin/env python
"""
admin.py - jenni Admin Module
Copyright 2010-2015, Michael Yanovich (yanovich.net), Alek Rollyson, Josh Begleiter (jbegleiter.com)
Licensed under the Eiffel Forum License 2.

More info:
 * jenni: https://github.com/myano/jenni/
 * Phenny: http://inamidst.com/phenny/

Beefed up by Alek Rollyson, Josh Begleiter.
* Added functions for op, deop, voice, devoice
* Uses NickServ ACC to verify that a nick is identified with services, as well
  as m5's admin list as a double verification system. Should eliminate the possibility
  of nick spoofing. May only work with freenode, hasn't been tested on other networks.
"""

import re

auth_list = []
admins = []
def is_chan_admin(jenni, input, a):
    chanadmin = False
    if hasattr(jenni.config, 'helpers'):
        if a in jenni.config.helpers and (input.host in jenni.config.helpers[a] or (input.nick).lower() in jenni.config.helpers[a]):
            chanadmin = True
    elif input.admin:
        chanadmin = True
    return chanadmin

def voice(jenni, input):
    """
    Command to voice users in a room. If no nick is given,
    jenni will voice the nick who sent the command
    """
    text = input.group().split()
    argc = len(text)
    if argc < 2: return
    opt = text[1]
    nick = opt
    channel = input.sender
    if opt.startswith('#'):
        if argc < 3: return
        nick = text[2]
        channel = opt
    if not is_chan_admin(jenni,input,channel):
        return jenni.say('You must be an admin to perform this operation')
    jenni.write(['MODE', channel, "+v", nick])
voice.commands = ['voice']
voice.priority = 'low'
voice.example = '.voice ##example or .voice ##example nick'

def devoice(jenni, input):
    """
    Command to devoice users in a room. If no nick is given,
    jenni will devoice the nick who sent the command
    """
    text = input.group().split()
    argc = len(text)
    if argc < 2: return
    opt = text[1]
    nick = opt
    channel = input.sender
    if opt.startswith('#'):
        if argc < 3: return
        nick = text[2]
        channel = opt
    if not is_chan_admin(jenni,input,channel):
        return jenni.say('You must be an admin to perform this operation')
    jenni.write(['MODE', channel, "-v", nick])
devoice.commands = ['devoice']
devoice.priority = 'low'
devoice.example = '.devoice ##example or .devoice ##example nick'

def op(jenni, input):
    """
    Command to op users in a room. If no nick is given,
    jenni will op the nick who sent the command
    """
    text = input.group().split()
    argc = len(text)
    if argc < 2: return
    opt = text[1]
    nick = opt
    channel = input.sender
    if opt.startswith('#'):
        if argc < 3: return
        nick = text[2]
        channel = opt
    if not is_chan_admin(jenni,input,channel):
        return jenni.say('You must be an admin to perform this operation')
    jenni.write(['MODE', channel, "+o", nick])
op.commands = ['op']
op.priority = 'low'
op.example = '.op ##example or .op ##example nick'

def deop(jenni, input):
    text = input.group().split()
    argc = len(text)
    if argc < 2: return
    opt = text[1]
    nick = opt
    channel = input.sender
    if opt.startswith('#'):
        if argc < 3: return
        nick = text[2]
        channel = opt
    if not is_chan_admin(jenni,input,channel):
        return jenni.say('You must be an admin to perform this operation')
    jenni.write(['MODE', channel, "-o", nick])
deop.commands = ['deop']
deop.priority = 'low'
deop.example = '.deop ##example or .deop ##example nick'

def auth_request(jenni, input):
    """
    This will scan every message in a room for nicks in jenni's
    admin list.  If one is found, it will send an ACC request
    to NickServ.  May only work with Freenode.
    """
    admins = jenni.config.admins
    pattern = '(' + '|'.join([re.escape(x) for x in admins]) + ')'
    matches = re.findall(pattern, input)
    for x in matches:
        jenni.msg('NickServ', 'ACC ' + x)
auth_request.rule = r'.*'
auth_request.priority = 'high'

def auth_verify(jenni, input):
    """
    This will wait for notices from NickServ and scan for ACC
    responses.  This verifies with NickServ that nicks in the room
    are identified with NickServ so that they cannot be spoofed.
    May only work with freenode.
    """
    global auth_list
    nick = input.group(1)
    level = input.group(3)
    if input.nick != 'NickServ':
        return
    elif level == '3':
        if nick in auth_list:
            return
        else:
            auth_list.append(nick)
    else:
        if nick not in auth_list:
            return
        else:
            auth_list.remove(nick)
auth_verify.event = 'NOTICE'
auth_verify.rule = r'(\S+) (ACC) ([0-3])'
auth_verify.priority = 'high'

def auth_check(jenni, nick, target=None):
    """
    Checks if nick is on the auth list and returns true if so
    """
    global auth_list
    if target == jenni.config.nick:
        return 0
    elif nick in auth_list:
        return 1

def deauth(nick):
    """
    Remove people from the deauth list.
    """
    global auth_list
    if nick in auth_list:
        a = auth_list.index(nick)
        del(auth_list[a])

def deauth_quit(jenni, input):
    deauth(input.nick)
deauth_quit.event = 'QUIT'
deauth_quit.rule = '.*'

def deauth_part(jenni, input):
    deauth(input.nick)
deauth_part.event = 'PART'
deauth_part.rule = '.*'

def deauth_nick(jenni, input):
    deauth(input.nick)
deauth_nick.event = 'NICK'
deauth_nick.rule = '.*'

def kick(jenni, input):
    if not input.admin: return
    text = input.group().split()
    argc = len(text)
    if argc < 2: return
    opt = text[1]
    nick = opt
    channel = input.sender
    reasonidx = 2
    if opt.startswith('#'):
        if argc < 3: return
        nick = text[2]
        channel = opt
        reasonidx = 3
    reason = ' '.join(text[reasonidx:])
    if nick != jenni.config.nick:
        jenni.write(['KICK', channel, nick, reason])
kick.commands = ['kick']
kick.priority = 'high'

def configureHostMask (mask, input):
    if mask == '*!*@*': return mask
    if re.match('^[^.@!/]+$', mask) is not None: return '*!*@%s' % input.host
    if re.match('^[^@!]+$', mask) is not None: return '*!*@%s' % mask

    m = re.match('^([^!@]+)@$', mask)
    if m is not None: return '*!%s@*' % m.group(1)

    m = re.match('^([^!@]+)@([^@!]+)$', mask)
    if m is not None: return '*!%s@%s' % (m.group(1), m.group(2))

    m = re.match('^([^!@]+)!(^[!@]+)@?$', mask)
    if m is not None: return '%s!%s@*' % (m.group(1), m.group(2))
    return ''

def ban (jenni, input):
    """
    This give admins the ability to ban a user.
    The bot must be a Channel Operator for this command to work.
    """
    text = input.group().split()
    argc = len(text)
    if argc < 2: return
    opt = text[1]
    banmask = opt
    channel = input.sender
    if opt.startswith('#'):
        if argc < 3: return
        channel = opt
        banmask = text[2]
    if not is_chan_admin(jenni,input,channel):
        return jenni.say('You must be an admin to perform this operation')
    banmask = configureHostMask(banmask, input)
    if banmask == '': return
    jenni.write(['MODE', channel, '+b', banmask])
ban.commands = ['ban']
ban.priority = 'high'

def unban (jenni, input):
    """
    This give admins the ability to unban a user.
    The bot must be a Channel Operator for this command to work.
    """
    text = input.group().split()
    argc = len(text)
    if argc < 2: return
    opt = text[1]
    banmask = opt
    channel = input.sender
    if opt.startswith('#'):
        if argc < 3: return
        channel = opt
        banmask = text[2]
    if not is_chan_admin(jenni,input,channel):
        return jenni.say('You must be an admin to perform this operation')
    banmask = configureHostMask(banmask, input)
    if banmask == '': return
    jenni.write(['MODE', channel, '-b', banmask])
unban.commands = ['unban']
unban.priority = 'high'

def quiet (jenni, input):
   """
   This gives admins the ability to quiet a user.
   The bot must be a Channel Operator for this command to work
   """
   text = input.group().split()
   argc = len(text)
   if argc < 2: return
   opt = text[1]
   banmask = opt
   channel = input.sender
   if opt.startswith('#'):
       if argc < 3: return
       channel = opt
       banmask = text[2]
   if not is_chan_admin(jenni, input, channel):
       return jenni.say('You must be an admin to perform this operation')
   quietmask = configureHostMask(banmask, input)
   if quietmask == '': return
   jenni.write(['MODE', channel, '+q', quietmask])
quiet.commands = ['quiet']
quiet.priority = 'high'

def unquiet (jenni, input):
   """
   This gives admins the ability to unquiet a user.
   The bot must be a Channel Operator for this command to work
   """
   text = input.group().split()
   argc = len(text)
   if argc < 2: return
   opt = text[1]
   banmask = opt
   channel = input.sender
   if opt.startswith('#'):
       if argc < 3: return
       channel = opt
       banmask = text[2]
   if not is_chan_admin(jenni, input, channel):
       return jenni.say('You must be an admin to perform this operation')
   quietmask = configureHostMask(banmask, input)
   if quietmask == '': return
   jenni.write(['MODE', channel, '-q', quietmask])
unquiet.commands = ['unquiet']
unquiet.priority = 'high'

def kickban (jenni, input):
   """
   This gives admins the ability to kickban a user.
   The bot must be a Channel Operator for this command to work
   .kickban [#chan] user1 user!*@* get out of here
   """
   text = input.group().split()
   argc = len(text)
   if argc < 4: return
   opt = text[1]
   channel = input.sender
   nick = opt
   mask = text[2]
   reasonidx = 3
   if opt.startswith('#'):
       if argc < 5: return
       channel = opt
       nick = text[2]
       mask = text[3]
       reasonidx = 4
   if not is_chan_admin(jenni, input, channel):
       return jenni.say('You must be an admin to perform this operation')
   reason = ' '.join(text[reasonidx:])
   mask = configureHostMask(mask)
   if mask == '': return
   jenni.write(['MODE', channel, '+b', mask])
   jenni.write(['KICK', channel, nick, ' :', reason])
kickban.commands = ['kickban', 'kb']
kickban.priority = 'high'

def topic(jenni, input):
    """
    This gives admins the ability to change the topic.
    Note: One does *NOT* have to be an OP, one just has to be on the list of
    admins.
    """
    text = input.group().split()
    argc = len(text)
    channel = input.sender
    topic = ' '.join(text[1:])
    if text[1].startswith('#'):
        if argc < 2: return
        channel = text[1]
        topic = ' '.join(text[2:])
    if topic == '':
        return
    jenni.write(['TOPIC', channel], topic)
    return
topic.commands = ['topic']
topic.priority = 'low'

if __name__ == '__main__':
    print __doc__.strip()
