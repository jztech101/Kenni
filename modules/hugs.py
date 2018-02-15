#!/usr/bin/env python2

def hugs(kenni, input):
    '''.hugs <nick> -- have kenni hug somebody'''
    txt = input.group(2)
    if not txt:
        msg = '\x01ACTION hugs %s\x01' % (input.nick)
        return kenni.msg(input.sender, msg, x=True)
    parts = txt.split()
    to = parts[0]
    if to == kenni.config.nick:
        to = 'themself'

    msg = '\x01ACTION hugs %s\x01' % (to)
    kenni.msg(input.sender, msg, x=True)
hugs.commands = ['hug', 'hugs']

if __name__ == '__main__':
    print __doc__.strip()
