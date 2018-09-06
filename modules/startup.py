#!/usr/bin/env python3
import threading, time, sys
import tools

def setup(kenni):
    # by clsn
    kenni.data = {}
    refresh_delay = 300.0

    if hasattr(kenni.config, 'refresh_delay'):
        try: refresh_delay = float(kenni.config.refresh_delay)
        except: pass

        def close():
            print("Nobody PONGed our PING, restarting")
            kenni.handle_close()

        def pingloop():
            timer = threading.Timer(refresh_delay, close, ())
            kenni.data['startup.setup.timer'] = timer
            kenni.data['startup.setup.timer'].start()
            # print "PING!"
            kenni.write(('PING', kenni.config.host))
        kenni.data['startup.setup.pingloop'] = pingloop

        def pong(kenni, input):
            try:
                # print "PONG!"
                kenni.data['startup.setup.timer'].cancel()
                time.sleep(refresh_delay + 60.0)
                pingloop()
            except: pass
        pong.event = 'PONG'
        pong.thread = True
        pong.rule = r'.*'
        kenni.variables['pong'] = pong

        # Need to wrap handle_connect to start the loop.
        inner_handle_connect = kenni.handle_connect

        def outer_handle_connect():
            inner_handle_connect()
            if kenni.data.get('startup.setup.pingloop'):
                kenni.data['startup.setup.pingloop']()

        kenni.handle_connect = outer_handle_connect

def startup(kenni, input):
    import time

    if hasattr(kenni.config, 'serverpass') and not kenni.auth_attempted:
        kenni.write(('PASS', kenni.config.serverpass))

    if not kenni.is_authenticated and hasattr(kenni.config, 'password'):
        if hasattr(kenni.config, 'user') and kenni.config.user is not None:
            user = kenni.config.user
        else:
            user = kenni.config.nick

        kenni.msg('NickServ', 'IDENTIFY %s %s' % (user, kenni.config.password))
        time.sleep(10)

    # Cf. http://swhack.com/logs/2005-12-05#T19-32-36
    for channel in kenni.channels:
        kenni.join(channel, None)
        time.sleep(0.5)
startup.rule = r'(.*)'
startup.event = '251'
startup.priority = 'low'


def nick(kenni,input):
    for channel in kenni.channels:
        kenni.write(['WHO', channel])
nick.rule = r'(.*)'
nick.event = 'NICK'
nick.priority = 'high'

def hostmask_on_join(kenni, input):
    if not input.mode or not tools.isChan(input.mode, False):
        return
    kenni.set_hostmask(input.other2.lower(), input.names)
    kenni.set_ident(input.other2.lower(), input.mode_target)
hostmask_on_join.rule = r'(.*)'
hostmask_on_join.event = '352'
hostmask_on_join.priority = 'high'

def new_Join_Hostmask(kenni, input):
    if not input.sender or not tools.isChan(input.sender, False):
        return
    kenni.set_hostmask(input.nick.lower(), input.host)
    kenni.set_ident(input.nick.lower(), input.user)
new_Join_Hostmask.rule = r'(.*)'
new_Join_Hostmask.event = 'JOIN'
new_Join_Hostmask.priority = 'high'

if __name__ == '__main__':
    print(__doc__.strip())
