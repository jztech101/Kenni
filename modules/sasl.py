#!/usr/bin/env python3
import base64

def irc_cap (kenni, input):
    cap, value = input.args[1], input.args[2]
    rq = ''

    if kenni.is_connected:
        return

    if cap == 'LS':
        if 'multi-prefix' in value:
            rq += ' multi-prefix'
        if 'sasl' in value:
            rq += ' sasl'

        if not rq:
            irc_cap_end(kenni, input)
        else:
            if rq[0] == ' ':
                rq = rq[1:]

            kenni.write(('CAP', 'REQ', ':' + rq))

    elif cap == 'ACK':
        if 'sasl' in value:
            kenni.write(('AUTHENTICATE', 'PLAIN'))
        else:
            irc_cap_end(kenni, input)

    elif cap == 'NAK':
        irc_cap_end(kenni, input)

    else:
        irc_cap_end(kenni, input)

    return
irc_cap.rule = r'(.*)'
irc_cap.event = 'CAP'
irc_cap.priority = 'high'


def irc_authenticated (kenni, input):
    auth = False
    if hasattr(kenni.config, 'nick') and kenni.config.nick is not None and hasattr(kenni.config, 'password') and kenni.config.password is not None:
        nick = kenni.config.nick
        password = kenni.config.password

        # If provided, use the specified user for authentication, otherwise just use the nick
        if hasattr(kenni.config, 'user') and kenni.config.user is not None:
            user = kenni.config.user
        else:
            user = nick

        auth = "\0".join((nick, user, password))
        auth = base64.b64encode(auth.encode('utf-8'))

    if not auth:
        kenni.write(('AUTHENTICATE', '+'))
    else:
        while len(auth) >= 400:
            out = auth[0:400]
            auth = auth[401:]
            kenni.write(('AUTHENTICATE', out))

        if auth:
            kenni.write(('AUTHENTICATE', auth))
        else:
            kenni.write(('AUTHENTICATE', '+'))

    return
irc_authenticated.rule = r'(.*)'
irc_authenticated.event = 'AUTHENTICATE'
irc_authenticated.priority = 'high'


def irc_903 (kenni, input):
    kenni.is_authenticated = True
    irc_cap_end(kenni, input)
    return
irc_903.rule = r'(.*)'
irc_903.event = '903'
irc_903.priority = 'high'


def irc_904 (kenni, input):
    irc_cap_end(kenni, input)
    return
irc_904.rule = r'(.*)'
irc_904.event = '904'
irc_904.priority = 'high'


def irc_905 (kenni, input):
    irc_cap_end(kenni, input)
    return
irc_905.rule = r'(.*)'
irc_905.event = '905'
irc_905.priority = 'high'


def irc_906 (kenni, input):
    irc_cap_end(kenni, input)
    return
irc_906.rule = r'(.*)'
irc_906.event = '906'
irc_906.priority = 'high'


def irc_907 (kenni, input):
    irc_cap_end(kenni, input)
    return
irc_907.rule = r'(.*)'
irc_907.event = '907'
irc_907.priority = 'high'


def irc_001 (kenni, input):
    kenni.is_connected = True
    return
irc_001.rule = r'(.*)'
irc_001.event = '001'
irc_001.priority = 'high'


def irc_cap_end (kenni, input):
    kenni.write(('CAP', 'END'))
    return


if __name__ == '__main__':
    print(__doc__.strip())
