#!/usr/bin/env python3
import os
import time
import tools

intentional_part = False

def join(kenni, input):
    '''Join the specified channel. This is an owner-only command.'''
    if not input.owner:
        return kenni.say('You do not have owner privs.')
    incoming = input.group(2)
    if not incoming:
        return kenni.say('Please provide some channels to join.')
    inc = incoming.split(' ')
    if len(inc) > 2:
        ## 3 or more inputs
        return kenni.say('Too many inputs.')
    if input.owner:
        channel = inc[0]
        key = str()
        if len(inc) > 1:
            ## 2 inputs
            key = inc[1]
        kenni.join(channel, key)
join.commands = ['join']
join.priority = 'medium'
join.example = '.join #example or .join #example key'

def part(kenni, input):
    '''Part the specified channel. This is an admin-only command.'''
    global intentional_part
    if input.admin:
        sendmessage = input.group(2)
        sendmessage2 = []
        if sendmessage:
            sendmessage2 = sendmessage.split(" ")
        intentional_part = True
        if tools.isChan(input.sender, False) and (not sendmessage or not tools.isChan(sendmessage2[0], False)):
            kenni.write(['PART', input.sender])
        else:
            kenni.write(['PART', sendmessage2[0] + " :" ' '.join(sendmessage2[1:])])
part.commands = ['part']
part.priority = 'medium'
part.example = '.part #example'

def cycle(kenni, input):
    '''Part the specified channel. This is an admin-only command.'''
    global intentional_part
    if input.admin:
        sendmessage = input.group(2)
        sendmessage2 = []
        if sendmessage:
            sendmessage2 = sendmessage.split(" ")
        intentional_part = True
        if tools.isChan(input.sender, False) and (not sendmessage or not tools.isChan(sendmessage2[0], False)):
            kenni.write(['PART'], input.sender)
            kenni.join(input.sender, None)
        else:
            kenni.write(['PART', sendmessage2[0]])
            kenni.join(sendmessage2[0], None)
cycle.commands = ['cycle']
cycle.priority = 'medium'
cycle.example = '.cycle #example'

def quit(kenni, input):
    '''Quit from the server. This is an owner-only command.'''
    if input.owner:
        kenni.write(['QUIT'])
        __import__('os')._exit(0)
quit.commands = ['quit']
quit.priority = 'low'


def msg(kenni, input):
    if input.owner:
        text = input.group().split()
        argc = len(text)
        channel = input.sender
        msg = ' '.join(text[1:])
        if argc > 2 and tools.isChan(text[1], True):
            channel = text[1]
            msg = ' '.join(text[2:])
        kenni.write(['PRIVMSG', channel], msg)
msg.commands = ['say']
msg.priority = 'low'

def act(kenni, input):
    if input.owner:
        text = input.group().split()
        argc = len(text)
        channel = input.sender
        msg = ' '.join(text[1:])
        if argc > 2 and tools.isChan(text[1], False):
            channel = text[1]
            msg = ' '.join(text[2:])
        kenni.write(['PRIVMSG', channel], '\x01ACTION ' + msg + '\x01')
act.commands = ['act', 'do']
act.priority = 'low'


def defend_ground(kenni, input):
    '''
    This function monitors all kicks across all channels kenni is in. If she
    detects that she is the one kicked she'll automatically join that channel.

    WARNING: This may not be needed and could cause problems if kenni becomes
    annoying. Please use this with caution.
    '''
    channel = input.sender
    kenni.join(channel, None)
    time.sleep(10)
    kenni.join(channel, None)
defend_ground.event = 'KICK'
defend_ground.rule = '.*'
defend_ground.priority = 'low'


def defend_ground2(kenni, input):
    global intentional_part
    if not intentional_part and input.nick == kenni.config.nick:
        intentional_part = False
        channel = input.sender
        kenni.join(channel, None)
        time.sleep(10)
        kenni.join(channel, None)
defend_ground2.event = 'PART'
defend_ground2.rule = '.*'
defend_ground2.priority = 'low'


def blocks(kenni, input):
    if not input.admin: return

    if hasattr(kenni.config, 'logchan_pm') and input.sender != kenni.config.logchan_pm:
        # BLOCKS USED - user in ##channel - text
        kenni.msg(kenni.config.logchan_pm, 'BLOCKS USED - %s in %s -- %s' % (input.nick, input.sender, input))

    STRINGS = {
            'success_del' : 'Successfully deleted block: %s',
            'success_add' : 'Successfully added block: %s',
            'no_nick' : 'No matching nick block found for: %s',
            'no_host' : 'No matching hostmask block found for: %s',
            'no_ident': 'No matching ident block found for: %s',
            'invalid' : 'Invalid format for %s a block. Try: .blocks add (nick|hostmask|ident) kenni',
            'invalid_display' : 'Invalid input for displaying blocks.',
            'nonelisted' : 'No %s listed in the blocklist.',
            'huh' : 'I could not figure out what you wanted to do.',
            }

    if not os.path.isfile('blocks'):
        blocks = open('blocks', 'w')
        blocks.write('\n')
        blocks.close()

    blocks = open('blocks', 'r')
    contents = blocks.readlines()
    blocks.close()

    try: masks = contents[0].replace('\n', '').split(',')
    except: masks = ['']

    try: nicks = contents[1].replace('\n', '').split(',')
    except: nicks = ['']

    try: idents = contents[2].replace('\n', '').split(',')
    except: idents = ['']

    text = input.group().split()

    if len(text) == 3 and text[1] == 'list':
        ## Display all contents of the following

        ## Hostmasks
        if text[2] == 'hostmask':
            if len(masks) > 0 and masks.count('') == 0:
                for each in masks:
                    if len(each) > 0:
                        kenni.say('blocked hostmask: ' + each)
            else:
                kenni.say(STRINGS['nonelisted'] % ('hostmasks'))

        ## Nicks
        elif text[2] == 'nick':
            if len(nicks) > 0 and nicks.count('') == 0:
                for each in nicks:
                    if len(each) > 0:
                        kenni.say('blocked nick: ' + each)
            else:
                kenni.say(STRINGS['nonelisted'] % ('nicks'))

        elif text[2] == 'ident':
            if len(idents) > 0 and idents.count('') == 0:
                for each in idents:
                    if len(each) > 0:
                        kenni.say('blocked ident: ' + each)

        ## Couldn't display anything
        else:
            kenni.say(STRINGS['invalid_display'])

    elif len(text) == 4 and text[1] == 'add':
        ## Add blocks...

        if text[2] == 'nick':
            nicks.append(text[3])
        elif text[2] == 'hostmask':
            masks.append(text[3])
        elif text[2] == 'ident':
            idents.append(text[3])
        else:
            kenni.say(STRINGS['invalid'] % ('adding'))
            return

        kenni.say(STRINGS['success_add'] % (text[3]))

    elif len(text) == 4 and text[1] == 'del':
        ## Delete a block...

        ## Nick
        if text[2] == 'nick':
            try:
                nicks.remove(text[3])
                kenni.say(STRINGS['success_del'] % (text[3]))
            except:
                kenni.say(STRINGS['no_nick'] % (text[3]))
                return

        ## Hostmask
        elif text[2] == 'hostmask':
            try:
                masks.remove(text[3])
                kenni.say(STRINGS['success_del'] % (text[3]))
            except:
                kenni.say(STRINGS['no_host'] % (text[3]))
                return

        ## Ident
        elif text[2] == 'ident':
            try:
                idents.remove(text[3])
                kenni.say(STRINGS['success_del'] % (text[3]))
            except:
                kenni.say(STRINGS['no_ident'] % (text[3]))
                return
        else:
            kenni.say(STRINGS['invalid'] % ('deleting'))
            return
    else:
        kenni.say(STRINGS['huh'])

    os.remove('blocks')
    blocks = open('blocks', 'w')

    masks_str = ','.join(masks)
    if len(masks_str) > 0 and ',' == masks_str[0]:
        masks_str = masks_str[1:]
    blocks.write(masks_str)

    blocks.write('\n')

    nicks_str = ','.join(nicks)
    if len(nicks_str) > 0 and ',' == nicks_str[0]:
        nicks_str = nicks_str[1:]
    blocks.write(nicks_str)

    blocks.write('\n')

    idents_str = ','.join(idents)
    if len(idents_str) > 0 and ',' == idents_str[0]:
        idents_str = idents_str[1:]
    blocks.write(idents_str)

    blocks.close()

blocks.commands = ['blocks']
blocks.priority = 'low'
blocks.thread = False

char_replace = {
        r'\x01': chr(1),
        r'\x02': chr(2),
        r'\x03': chr(3),
        }

def write_raw(kenni, input):
    if not input.owner: return
    txt = input.bytes[5:]
    txt = txt.decode('utf-8')
    a = txt.split(':')
    status = False
    if len(a) > 1:
        newstr = ':'.join(a[1:])
        for x in char_replace:
            if x in newstr:
                newstr = newstr.replace(x, char_replace[x])
        kenni.write(a[0].split(), newstr, raw=True)
        status = True
    elif a:
        b = a[0].split()
        kenni.write([b[0].strip()], ' '.join(b[1:]), raw=True)
        status = True
    if status:
        kenni.say('Message sent to server.')
write_raw.commands = ['raw']
write_raw.priority = 'high'
write_raw.thread = False

if __name__ == '__main__':
    print(__doc__.strip())

