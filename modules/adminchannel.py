#!/usr/bin/env python3
import re
import tools

def is_chan_admin(kenni, input, a):
    if input.admin:
        return True
    elif hasattr(kenni.config, 'helpers'):
        if a in kenni.config.helpers and input.host in kenni.config.helpers[a]:
            return True
    return False

def voice(kenni, input):
    """
    Command to voice users in a room. If no nick is given,
    kenni will voice the nick who sent the command
    """
    text = input.group().split()
    argc = len(text)
    nick = input.nick
    channel = input.sender
    if not tools.isChan(input.sender, False):
        channel = None
    if argc >= 2 and text[1] is not None:
        if tools.isChan(text[1], False):
            channel = text[1]
            if argc >= 3 and text[2] is not None:
                nick = text[2]
        else:
            nick = text[1]
    if channel is not None:
        if not is_chan_admin(kenni,input,channel):
            return kenni.say('You must be an admin to perform this operation')
        kenni.write(['MODE', channel, "+v", nick])
voice.commands = ['voice']
voice.priority = 'low'
voice.example = '.voice ##example or .voice ##example nick'

def mode(kenni, input):
    """
    """
    text = input.group().split()
    argc = len(text)
    channel = input.sender
    if not tools.isChan(input.sender, False):
        channel = None
    if argc >= 2 and text[1] is not None:
        if tools.isChan(text[1], False):
            channel = text[1]
            if argc >= 3 and text[2] is not None:
                modex = " ".join(text[2:])
        else:
            modex = " ".join(text[1:])
    if channel is not None:
        if not is_chan_admin(kenni,input,channel):
            return kenni.say('You must be an admin to perform this operation')
        kenni.write(['MODE', channel, modex])
mode.commands = ['mode']
mode.priority = 'low'

def invite(kenni, input):
    """
    Command to voice users in a room. If no nick is given,
    kenni will voice the nick who sent the command
    """
    text = input.group().split()
    argc = len(text)
    nick = input.nick
    channel = input.sender
    if not tools.isChan(input.sender, False):
        channel = None
    if argc >= 2 and text[1] is not None:
        if tools.isChan(text[1], False):
            channel = text[1]
            if argc >= 3 and text[2] is not None:
                nick = text[2]
        else:
            nick = text[1]
    if channel is not None:
        if not is_chan_admin(kenni,input,channel):
            return kenni.say('You must be an admin to perform this operation')
        kenni.write(['PRIVMSG', channel], '\x01ACTION invites ' + nick + ' per ' + input.nick + '\x01')
        kenni.write(['INVITE', nick], channel)
invite.commands = ['invite']
invite.priority = 'low'

def devoice(kenni, input):
    """
    Command to devoice users in a room. If no nick is given,
    kenni will devoice the nick who sent the command
    """
    text = input.group().split()
    argc = len(text)
    nick = input.nick
    channel = input.sender
    if not tools.isChan(input.sender, False):
        channel = None
    if argc >= 2 and text[1] is not None:
        if tools.isChan(text[1], False):
            channel = text[1]
            if argc >= 3 and text[2] is not None:
                nick = text[2]
        else:
            nick = text[1]
    if channel is not None:
        if not is_chan_admin(kenni,input,channel):
            return kenni.say('You must be an admin to perform this operation')
        kenni.write(['MODE', channel, "-v", nick])
devoice.commands = ['devoice']
devoice.priority = 'low'
devoice.example = '.devoice ##example or .devoice ##example nick'

def op(kenni, input):
    """
    Command to op users in a room. If no nick is given,
    kenni will op the nick who sent the command
    """
    text = input.group().split()
    argc = len(text)
    nick = input.nick
    channel = input.sender
    if not tools.isChan(input.sender, False):
        channel = None
    if argc >= 2 and text[1] is not None:
        if tools.isChan(text[1], False):
            channel = text[1]
            if argc >= 3 and text[2] is not None:
                nick = text[2]
        else:
            nick = text[1]
    if channel is not None:
        if not is_chan_admin(kenni,input,channel):
            return kenni.say('You must be an admin to perform this operation')
        kenni.write(['MODE', channel, "+o", nick])
op.commands = ['op']
op.priority = 'low'
op.example = '.op ##example or .op ##example nick'

def deop(kenni, input):
    text = input.group().split()
    argc = len(text)
    nick = input.nick
    channel = input.sender
    if not tools.isChan(input.sender, False):
        channel = None
    if argc >= 2 and text[1] is not None:
        if tools.isChan(text[1], False):
            channel = text[1]
            if argc >= 3 and text[2] is not None:
                nick = text[2]
        else:
            nick = text[1]
    if channel is not None:
        if not is_chan_admin(kenni,input,channel):
            return kenni.say('You must be an admin to perform this operation')
        kenni.write(['MODE', channel, "-o", nick])
deop.commands = ['deop']
deop.priority = 'low'
deop.example = '.deop ##example or .deop ##example nick'

def kick(kenni, input):
    text = input.group().split()
    argc = len(text)
    channel = input.sender
    opt = text[1]
    nick = opt
    reasonidx = "Your behavior is not conductive to the desired environment"
    if tools.isChan(opt, False):
        channel = opt
        nick = text[2]
        if (argc > 3):
            reasonidx = " ".join(text[3:])
    else:
        if (argc > 2):
            reasonidx = " ".join(text[2:])
    if not is_chan_admin(kenni, input, channel):
        return kenni.say('You must be an admin to perform this operation')
    if "," in nick:
        nicks = nick.split(",")
        for nic in nicks:
            kickx(kenni, channel, nic, input.nick, reasonidx)
    else:
        kickx(kenni, channel, nick, input.nick, reasonidx)
kick.commands = ['kick']
kick.priority = 'high'

def kickx(kenni, channel, nick, sender, reasonidx):
    if nick == kenni.nick:
        nick = sender
    kenni.write(['KICK', channel, nick, ' :', "[" + sender + "] " + reasonidx])

def configureHostMask (mask, kenni):
    if "!" not in mask and "@" not in mask and ":" not in mask:
        ident = kenni.idents[mask]
        host = kenni.hostmasks[mask]
        if "~" not in ident:
            return "*!" + ident + "@" + host
        else:
            return "*!*@" + host
    else:
        return mask

def ban (kenni, input):
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
    if tools.isChan(opt, False):
        if argc < 3: return
        channel = opt
        banmask = text[2]
    if not is_chan_admin(kenni,input,channel):
        return kenni.say('You must be an admin to perform this operation')
    banmask = configureHostMask(banmask, kenni)
    if banmask == '': return
    kenni.write(['MODE', channel, '+b', banmask])
ban.commands = ['ban']
ban.priority = 'high'

def unban (kenni, input):
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
    if tools.isChan(opt, False):
        if argc < 3: return
        channel = opt
        banmask = text[2]
    if not is_chan_admin(kenni,input,channel):
        return kenni.say('You must be an admin to perform this operation')
    banmask = configureHostMask(banmask, kenni)
    if banmask == '': return
    kenni.write(['MODE', channel, '-b', banmask])
unban.commands = ['unban']
unban.priority = 'high'

def quiet (kenni, input):
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
   if tools.isChan(opt, False):
       if argc < 3: return
       channel = opt
       banmask = text[2]
   if not is_chan_admin(kenni, input, channel):
       return kenni.say('You must be an admin to perform this operation')
   quietmask = configureHostMask(banmask, kenni)
   if quietmask == '': return
   kenni.write(['MODE', channel, '+q', quietmask])
quiet.commands = ['quiet']
quiet.priority = 'high'

def unquiet (kenni, input):
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
   if tools.isChan(opt, False):
       if argc < 3: return
       channel = opt
       banmask = text[2]
   if not is_chan_admin(kenni, input, channel):
       return kenni.say('You must be an admin to perform this operation')
   quietmask = configureHostMask(banmask, kenni)
   if quietmask == '': return
   kenni.write(['MODE', channel, '-q', quietmask])
unquiet.commands = ['unquiet']
unquiet.priority = 'high'

def kickban (kenni, input):
   """
   This gives admins the ability to kickban a user.
   The bot must be a Channel Operator for this command to work
   .kickban [#chan] user1 user!*@* get out of here
   """
   text = input.group().split()
   argc = len(text)
   channel = input.sender
   opt = text[1]
   nick = opt
   reasonidx = "Your behavior is not conductive to the desired environment"
   if tools.isChan(opt, False):
       channel = opt
       nick = text[2]
       if(argc >3):
           reasonidx = " ".join(text[3:])
   else:
       if(argc >2):
           reasonidx = " ".join(text[2:])
   if not is_chan_admin(kenni, input, channel):
       return kenni.say('You must be an admin to perform this operation')
   mask = configureHostMask(nick,kenni)
   if mask == '': return
   kenni.write(['MODE', channel, '+b', mask])
   kickx(kenni, channel, nick, input.nick, reasonidx)
kickban.commands = ['kickban', 'kb', 'kban']
kickban.priority = 'high'

def topic(kenni, input):
    """
    This gives admins the ability to change the topic.
    Note: One does *NOT* have to be an OP, one just has to be on the list of
    admins.
    """
    text = input.group().split()
    argc = len(text)
    channel = input.sender
    topic = ' '.join(text[1:])
    if tools.isChan(text[1], False):
        if argc < 2: return
        channel = text[1]
        topic = ' '.join(text[2:])
    if not is_chan_admin(kenni,input,channel):
        return kenni.say('You must be an admin to perform this operation')
    if topic == '':
        return
    kenni.write(['TOPIC', channel], topic)
    return
topic.commands = ['topic']
topic.priority = 'low'

if __name__ == '__main__':
    print(__doc__.strip())
