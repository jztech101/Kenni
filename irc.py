#!/usr/bin/env python3
from __future__ import unicode_literals, absolute_import, print_function, division
import sys, re, time, traceback
import socket, asyncore, asynchat, ssl, select
import os, codecs
import errno
import tools

IRC_CODES = ('001', '002', '003','004', '005', '253', '251', '252', '254', '255', '265', '266', '250', '315', '328', '332', '333', '352', '353', '366', '372', '375', '376', 'QUIT', 'NICK', 'JOIN')
cwd = os.getcwd()

class Origin(object):
    source = re.compile(r'([^!]*)!?([^@]*)@?(.*)')

    def __init__(self, bot, source, args):
        match = Origin.source.match(source or '')
        self.nick, self.user, self.host = match.groups()

        target = mode = mode_target = names = other = other2 = None

        arg_len = len(args)
        if arg_len > 1:
            target = args[1]
            if arg_len > 2:
                mode = args[2]
                if arg_len > 3:
                    mode_target = args[3]
                    if arg_len > 4:
                        names = args[4]
                        if arg_len > 5:
                            other = args[5]
                            if arg_len > 6:
                                other2 = args[6]
        mappings = {bot.nick: self.nick, None: None}
        self.sender = mappings.get(target, target)
        self.mode = mode
        self.mode_target = mode_target
        self.names = names
        self.other = other
        self.other2 = other2
        self.other3 = target
        self.full_ident = source

def create_logdir():
    try: os.mkdir(cwd + "/logs")
    except Exception as e:
        print('There was a problem creating the logs directory.', file=sys.stderr)
        print(e.__class__, str(e), file=sys.stderr)
        print('Please fix this and then run kenni again.', file=sys.stderr)
        sys.exit(1)

def check_logdir():
    if not os.path.isdir(cwd + "/logs"):
        create_logdir()

def log_raw(line):
    check_logdir()
    f = codecs.open(cwd + "/logs/raw.log", 'a', encoding='utf-8')
    f.write(str(time.time()) + "\t")
    temp = line.replace('\n', '')
    try:
        temp = temp.decode('utf-8')
    except UnicodeDecodeError:
        try:
            temp = temp.decode('iso-8859-1')
        except UnicodeDecodeError:
            temp = temp.decode('cp1252')
    f.write(temp)
    f.write("\n")
    f.close()

class Bot(asynchat.async_chat):
    def __init__(self, nick, ident,  name, channels, user=None, password=None, logchan_pm=None, logging=False, ipv6=False):
        asynchat.async_chat.__init__(self)
        self.set_terminator(b'\n')
        self.buffer = ''

        self.nick = nick
        self.ident = ident
        if user is not None:
            self.user = user
        else:
            self.user = nick
        self.name = name
        self.password = password

        # Right now, only accounting for two op levels.
        # These lists are filled in startup.py
        self.ops = dict()
        self.hops = dict()
        self.voices = dict()

        self.use_ssl = False
        self.use_sasl = False
        self.is_connected = False

        # Store this separately from authenticated
        # that way we don't try twice
        self.auth_attempted = False
        self.is_authenticated = False

        self.verbose = True
        self.channels = channels or list()
        self.stack = list()
        self.hostmasks = dict()
        self.idents = dict()
        self.stack_log = list()
        self.logchan_pm = logchan_pm
        self.logging = logging
        self.ipv6 = ipv6

        import threading
        self.sending = threading.RLock()

    # def push(self, *args, **kargs):
    #     asynchat.async_chat.push(self, *args, **kargs)

    def handle_error(self):
        '''Handle any uncaptured error in the core. Overrides asyncore's handle_error
        This prevents the bot from disconnecting when it use to say something twice
        and then disconnect.'''
        trace = traceback.format_exc()
        try:
            print(trace)
        except Exception as e:
            print('Uncaptured error!!!', e)


    def __write(self, args, text=None, raw=False):
        # print '%r %r %r' % (self, args, text)
        try:
            args = [self.safe(arg) for arg in args]
            if text is not None:
                text = self.safe(text)
            if raw:
                temp = ' '.join(args)[:510] + " :" + text + '\r\n'
            elif not raw:
                if text:
                    # 510 because CR and LF count too, as nyuszika7h points out
                    temp = (' '.join(args) + ' :' + text)[:510] + '\r\n'
                else:
                    temp = ' '.join(args)[:510] + '\r\n'
            self.send(temp.encode('utf-8'))
        except Exception as e:
            print(time.time())
            print('[__WRITE FAILED]', e)
            sys.exit(0)

    def write(self, args, text=None, raw=False):
        try:
            args = [self.safe(arg) for arg in args]
            if text is not None:
                text = self.safe(text)
            if raw:
                self.__write(args, text, raw)
            else:
                self.__write(args, text)
        except Exception as e:
            print('[WRITE FAILED]', e)
    def join(self, channel, key):
        if not key:
            self.write(['JOIN'], channel)
        else:
            self.write(['JOIN', channel, key])
        self.write(['WHO', channel])


    def safe(self, string):
        """Remove newlines string."""
        if sys.version_info.major >= 3 and isinstance(string, bytes):
                string = string.decode('utf8')
        elif sys.version_info.major < 3:
            if not isinstance(string, str):
                string = str(string, encoding='utf8')
        string = string.replace('\n', '')
        string = string.replace('\r', '')
        return string

    def run(self, host, port=6667):
        self.initiate_connect(host, port)

    def initiate_connect(self, host, port):
        if self.verbose:
            message = 'Connecting to %s:%s...' % (host, port)
            print(message, end=' ', file=sys.stderr)

        if self.use_ssl:
            self.send = self._ssl_send
            self.recv = self._ssl_recv

        if self.ipv6:
            for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
                af, socktype, proto, canonname, sa = res
                try:
                    self.create_socket(af,socktype)
                except socket.error as msg:
                    continue
                try:
                    self.connect(sa)
                except socket.error as msg:
                    self.close()
                    continue
                break
            else:
                raise Exception("No connectivity")
        else:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect((host, port))

        try: asyncore.loop()
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            print('[asyncore]', e)

    def handle_connect(self):
        if self.use_ssl:
            self.ssl = ssl.wrap_socket(self.socket, do_handshake_on_connect=False, suppress_ragged_eofs=True)
            while True:
                try:
                    self.ssl.do_handshake()
                    break
                except ssl.SSLError as err:
                    if err.args[0] == ssl.SSL_ERROR_WANT_READ:
                        select.select([self.ssl], [], [])
                    elif err.args[0] == ssl.SSL_ERROR_WANT_WRITE:
                        select.select([], [self.ssl], [])
                    else:
                        raise
                except:
                    continue
            self.set_socket(self.ssl)

        if self.verbose:
            print('connected!', file=sys.stderr)

        if self.use_sasl:
            self.write(('CAP', 'LS'))

        if not self.use_sasl and self.password:
            self.write(('PASS', self.password))
            # Store the fact that we authed, or at least tried
            self.auth_attempted = True
        self.write(('NICK', self.nick))
        self.write(('USER', self.ident, '+iw', self.nick), self.name)

    def handle_close(self):
        self.close()
        print('Closed!', file=sys.stderr)

    def _ssl_send(self, data):
        """Replacement for self.send() during SSL connections."""
        try:
            result = self.socket.send(data)
            return result
        except ssl.SSLError as why:
            if why[0] in (asyncore.EWOULDBLOCK, errno.ESRCH):
                return 0
            else:
                raise why
            return 0

    def _ssl_recv(self, buffer_size):
        """Replacement for self.recv() during SSL connections.
        From: http://evanfosmark.com/2010/09/ssl-support-in-asynchatasync_chat
        """
        try:
            data = self.socket.read(buffer_size)
            if not data:
                self.handle_close()
                return b''
            return data
        except ssl.SSLError as why:
            if type(why) is ssl.SSLWantReadError:
                return b''
            elif why[0] in (asyncore.ECONNRESET, asyncore.ENOTCONN,
                          asyncore.ESHUTDOWN):
                self.handle_close()
                return b''
            elif why[0] == errno.ENOENT:
                # Required in order to keep it non-blocking
                return b''
            else:
                raise

    def collect_incoming_data(self, data):
        # We can't trust clients to pass valid str.
        try:
            data = str(data, encoding='utf-8')
        except UnicodeDecodeError:
            # not str, let's try cp1252
            try:
                data = str(data, encoding='cp1252')
            except UnicodeDecodeError:
                # Okay, let's try ISO8859-1
                try:
                    data = str(data, encoding='iso8859-1')
                except:
                    # Discard line if encoding is unknown
                    return

        self.buffer += data

    def found_terminator(self):
        line = self.buffer

        if line.endswith('\r'):
            line = line[:-1]

        if line:
            if self.logchan_pm:
                ## if logging to logging channel is enabled
                ## send stuff in PM to logging channel
                dlist = line.split()
                if len(dlist) >= 3:
                    if (not tools.isChan(dlist[2],True) or dlist[1].strip() == 'NOTICE') and dlist[1].strip() not in IRC_CODES:
                        if dlist[1].strip() == 'NOTICE':
                            if tools.isChan(dlist[2],True):
                                self.msg(self.logchan_pm, '[Notice] ' + dlist[0].replace(':','') + ': (' + dlist[2] + ') ' + ' '.join(dlist[3:]).replace(":",""), True)
                            else:
                                self.msg(self.logchan_pm, '[Notice] ' + dlist[0].replace(":","") + ': ' + ' '.join(dlist[3:]).replace(":",""), True)
                        elif dlist[1].strip() == 'PRIVMSG' and dlist[2].isalnum():
                            self.msg(self.logchan_pm, '[PM] ' + dlist[0].replace(":","") + ': ' + ' '.join(dlist[3:]).replace(":",""), True)
                        elif dlist[1].strip() == 'INVITE':
                            self.msg(self.logchan_pm, '[Invite] ' + dlist[0].replace(":","") + ': ' + dlist[3].replace(":",""), True)
                        else:
                            self.msg(self.logchan_pm, line, True)
            if self.logging:
                ## if logging (to log file) is enabled
                ## send stuff to the log file
                log_raw(line)

        self.buffer = ''

        # print line
        if line.startswith(':'):
            source, line = line[1:].split(' ', 1)
        else:
            source = None

        if ' :' in line:
            argstr, text = line.split(' :', 1)
            args = argstr.split()
            args.append(text)
        else:
            args = line.split()
            text = args[-1]

        origin = Origin(self, source, args)
        self.dispatch(origin, tuple([text] + args))

        if args[0] == 'PING':
            self.write(('PONG', text))


    def dispatch(self, origin, args):
        pass

    def msg(self, recipient, text, log=False, x=False, wait_time=3):
        self.sending.acquire()

        # Cf. http://swhack.com/logs/2006-03-01#T19-43-25
        if isinstance(text, str):
            try: text = text.encode('utf-8')
            except UnicodeDecodeError as e:
                text = e.__class__ + ': ' + str(e)
        if isinstance(recipient, str):
            try: recipient = recipient.encode('utf-8')
            except UnicodeDecodeError as e:
                return

        if not x:
            text = text.replace(b'\x01', b'')

        if wait_time < 1: wait_time = 1

        # No messages within the last 3 seconds? Go ahead!
        # Otherwise, wait so it's been at least 0.8 seconds + penalty
        def wait(sk, txt):
            if sk:
                elapsed = time.time() - sk[-1][0]
                if elapsed < wait_time:
                    penalty = float(max(0, len(txt) - 50)) / 70
                    wait = 0.8 + penalty
                    if elapsed < wait:
                        time.sleep(wait - elapsed)
        if log:
            wait(self.stack_log, text)
        else:
            wait(self.stack, text)

        '''
        # Loop detection
        if not log:
            messages = [m[1] for m in self.stack[-8:]]
            if messages.count(text) >= 5:
                text = '...'
                if messages.count('...') >= 3:
                    self.sending.release()
                    return
        '''

        self.__write(('PRIVMSG', self.safe(recipient)), self.safe(text))
        if log:
            self.stack_log.append((time.time(), text))
        else:
            self.stack.append((time.time(), text))
        self.stack = self.stack[-10:]
        self.stack_log = self.stack_log[-10:]

        self.sending.release()

    def notice(self, dest, text):
        self.write(('NOTICE', dest), text)

    def error(self, origin):
        try:
            import traceback
            trace = traceback.format_exc()
            print(trace)
            lines = list(reversed(trace.splitlines()))

            report = [lines[0].strip()]
            for line in lines:
                line = line.strip()
                if line.startswith('File "/'):
                    report.append(line[0].lower() + line[1:])
                    break
            else: report.append('source unknown')

            self.msg(origin.sender, report[0] + ' (' + report[1] + ')')
        except: self.msg(origin.sender, "Got an error.")

    # Functions to add/remove ops, hops, and voices
    def add_op(self, channel, name):
        if channel in self.ops:
            self.ops[channel].add(name)
        else:
            self.ops[channel] = set([name])
    def set_hostmask(self, name, hostmask):
        if name not in self.hostmasks:
            self.hostmasks[name] = hostmask
        elif self.hostmasks[name] != hostmask:
            self.hostmasks[name] = hostmask
    
    def set_ident(self, name, ident):
        if name not in self.idents:
            self.idents[name] = ident
        elif self.idents[name] != ident:
            self.idents[name] = ident

    def add_halfop(self, channel, name):
        if channel in self.hops:
            self.hops[channel].add(name)
        else:
            self.hops[channel] = set([name])

    def add_voice(self, channel, name):
        if channel in self.voices:
            self.voices[channel].add(name)
        else:
            self.voices[channel] = set([name])

    def del_op(self, channel, name):
        try: self.ops[channel].remove(name)
        except: pass

    def del_halfop(self, channel, name):
        try: self.hops[channel].remove(name)
        except: pass

    def del_voice(self, channel, name):
        try: self.voices[channel].remove(name)
        except: pass

class TestBot(Bot):
    def f_ping(self, origin, match, args):
        delay = m.group(1)
        if delay is not None:
            import time
            time.sleep(int(delay))
            self.msg(origin.sender, 'pong (%s)' % delay)
        else: self.msg(origin.sender, 'pong')
    f_ping.rule = r'^\.ping(?:[ \t]+(\d+))?$'

def main():
    # bot = TestBot('testbot', ['#d8uv.com'])
    # bot.run('irc.freenode.net')
    print(__doc__)

if __name__ == "__main__":
    main()
