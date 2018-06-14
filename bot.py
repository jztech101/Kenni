#!/usr/bin/env python3
import time, sys, os, re, threading, imp
import irc, os
import traceback

home = os.getcwd()

class kenni(irc.Bot):
    def __init__(self, config):
        lc_pm = None
        if hasattr(config, "logchan_pm"): lc_pm = config.logchan_pm
        logging = False
        if hasattr(config, "logging"): logging = config.logging
        ipv6 = False
        if hasattr(config, 'ipv6'): ipv6 = config.ipv6
        serverpass = None
        if hasattr(config, 'serverpass'): serverpass = config.serverpass
        user = None
        if hasattr(config, 'user'): user = config.user
        args = (config.nick, config.ident,  config.name, config.channels, user, serverpass, lc_pm, logging, ipv6)
        ## next, try putting a try/except around the following line
        irc.Bot.__init__(self, *args)
        self.config = config
        self.doc = {}
        self.stats = {}
        self.times = {}
        self.excludes = {}
        if hasattr(config, 'excludes'):
            self.excludes = config.excludes
        self.setup()

    def setup(self):
        self.variables = {}

        filenames = []

        # Default module folder + extra folders
        module_folders = [os.path.join(home, 'modules')]
        module_folders.extend(getattr(self.config, 'extra', []))

        excluded = getattr(self.config, 'exclude', [])
        enabled = getattr(self.config, 'enable', [])

        for folder in module_folders:
            if os.path.isfile(folder):
                filenames.append(folder)
            elif os.path.isdir(folder):
                for fn in os.listdir(folder):
                    if fn.endswith('.py') and not fn.startswith('_'):
                        name = os.path.basename(fn)[:-3]
                        # If whitelist is present only include whitelisted
                        # Never include blacklisted items
                        if name in enabled or not enabled and name not in excluded:
                            filenames.append(os.path.join(folder, fn))

        modules = []
        for filename in filenames:
            name = os.path.basename(filename)[:-3]
            # if name in sys.modules:
            #     del sys.modules[name]
            try: module = imp.load_source(name, filename)
            except Exception as e:
                print("Error loading %s: %s (in bot.py)" % (name, e), file=sys.stderr)
                traceback.print_exc()
            else:
                if hasattr(module, 'setup'):
                    module.setup(self)
                self.register(vars(module))
                modules.append(name)

        if modules:
            print('Registered modules:', ', '.join(sorted(modules)), file=sys.stderr)
        else:
            print("Warning: Couldn't find any modules", file=sys.stderr)

        self.bind_commands()

    def register(self, variables):
        # This is used by reload.py, hence it being methodised
        for name, obj in variables.items():
            if hasattr(obj, 'commands') or hasattr(obj, 'rule'):
                self.variables[name] = obj

    def bind_commands(self):
        self.rules = {'high': {}, 'medium': {}, 'low': {}}
        self.commands = {'high': {}, 'medium': {}, 'low': {}}
        self.commandrules = {'high': {}, 'medium': {}, 'low': {}}

        def bind_rules(self, priority, regexp, func):
            # register documentation
            if not hasattr(func, 'name'):
                func.name = func.__name__
            if func.__doc__:
                if hasattr(func, 'example'):
                    example = func.example
                    example = example.replace('$nickname', self.nick)
                else: example = None
                self.doc[func.name] = (func.__doc__, example)
            self.rules[priority].setdefault(regexp, []).append(func)

        def bind_command(self, priority, command, func):
            # register documentation
            if not hasattr(func, 'name'):
                func.name = func.__name__
            if func.__doc__:
                if hasattr(func, 'example'):
                    example = func.example
                    example = example.replace('$nickname', self.nick)
                else: example = None
                self.doc[func.name] = (func.__doc__, example)
            self.commands[priority].setdefault(command, []).append(func)
        def bind_commandrule(self, priority, command, func):
            # register documentation
            if not hasattr(func, 'name'):
                func.name = func.__name__
            if func.__doc__:
                if hasattr(func, 'example'):
                    example = func.example
                    example = example.replace('$nickname', self.nick)
                else: example = None
                self.doc[func.name] = (func.__doc__, example)
            self.commandrules[priority].setdefault(command, []).append(func)


        def sub(pattern, self=self):
            # These replacements have significant order
            pattern = pattern.replace('$nickname', re.escape(self.nick))
            return pattern.replace('$nick', r'%s[,:] +' % re.escape(self.nick))

        for name, func in self.variables.items():
            # print name, func
            if not hasattr(func, 'priority'):
                func.priority = 'medium'

            if not hasattr(func, 'thread'):
                func.thread = True

            if not hasattr(func, 'event'):
                func.event = 'PRIVMSG'
            else:
                if func.event:
                    func.event = func.event.upper()
                else:
                    continue

            if not hasattr(func, 'rate'):
                if hasattr(func, 'commands'):
                    func.rate = 3
                else:
                    func.rate = -1

            if hasattr(func, 'rule'):
                if isinstance(func.rule, str):
                    pattern = sub(func.rule)
                    regexp = re.compile(pattern)
                    bind_rules(self, func.priority, regexp, func)

                if isinstance(func.rule, tuple):
                    # 1) e.g. ('$nick', '(.*)')
                    if len(func.rule) == 2 and isinstance(func.rule[0], str):
                        prefix, pattern = func.rule
                        prefix = sub(prefix)
                        regexp = re.compile(prefix + pattern)
                        bind_rules(self, func.priority, regexp, func)

                    # 2) e.g. (['p', 'q'], '(.*)')
                    elif len(func.rule) == 2 and isinstance(func.rule[0], list):
                        commands, pattern = func.rule
                        for command in commands:
                            command = r'(?i)(%s)\b(?: +(?:%s))?' % (command, pattern)
                            bind_commandrule(self, func.priority, command, func)

                    # 3) e.g. ('$nick', ['p', 'q'], '(.*)')
                    elif len(func.rule) == 3:
                        prefix, commands, pattern = func.rule
                        prefix = sub(prefix)
                        for command in commands:
                            command = r'(?i)(%s) +' % command
                            regexp = re.compile(prefix + command + pattern)
                            bind_rules(self, func.priority, regexp, func)

            if hasattr(func, 'commands'):
                for command in func.commands:
                    bind_command(self, func.priority, command, func)
    def wrapped(self, origin, text, match):
        class kenniWrapper(object):
            def __init__(self, kenni):
                self._bot = kenni

            def __getattr__(self, attr):
                sender = origin.sender or text
                if attr == 'say':
                    return lambda msg: self._bot.msg(sender, msg)
                return getattr(self._bot, attr)

            def __setattr__(self, attr, value):
                if attr in ('_bot',):
                    # Explicitly allow the wrapped class to be set during __init__()
                    return super(kenniWrapper, self).__setattr__(attr, value)
                else:
                    # All other attributes will be set on the wrapped class transparently
                    return setattr(self._bot, attr, value)

        return kenniWrapper(self)

    def input(self, origin, text, match, event, args):
        class CommandInput(str):
            def __new__(cls, text, origin, match, event, args):
                s = str.__new__(cls, text)
                s.sender = origin.sender
                s.nick = origin.nick
                s.event = event
                s.bytes = text.encode('utf-8')
                s.match = match
                s.group = match.group
                s.groups = match.groups
                s.user = origin.user
                s.raw = origin
                s.args = args
                s.mode = origin.mode
                s.mode_target = origin.mode_target
                s.other = origin.other
                s.other2 = origin.other2
                s.other3 = origin.other3
                s.names = origin.names
                s.full_ident = origin.full_ident
                s.admin = origin.nick in self.config.admins
                if s.admin == False:
                    for each_admin in self.config.admins:
                        if each_admin == origin.host:
                            s.admin = True
                        elif '@' in each_admin:
                            if origin.nick + '@' + origin.host == each_admin:
                                s.admin = True
                s.chanadmin = False
                if hasattr(self.config, 'helpers'):
                    if origin.sender in self.config.helpers and origin.host in self.config.helpers[origin.sender]:
                        s.chanadmin = True
                if '@' in self.config.owner:
                   s.owner = origin.nick + '@' + origin.host == self.config.owner
                else:
                   s.owner = origin.host == self.config.owner
                s.host = origin.host
                return s

        return CommandInput(text, origin, match, event, args)

    def call(self, func, origin, kenni, input):
        nick = (input.nick).lower()
        try:
            if hasattr(self, 'excludes'):
                if (input.sender).lower() in self.excludes:
                    if '!' in self.excludes[(input.sender).lower()]:
                        # block all function calls for this channel
                        return
                    fname = func.__code__.co_filename.split('/')[-1].split('.')[0]
                    if fname in self.excludes[(input.sender).lower()]:
                        # block function call if channel is blacklisted
                        return
        except Exception as e:
            print("Error attempting to block:", str(func.name))
            self.error(origin)

        try:
            func(kenni, input)
        except Exception as e:
            self.error(origin)

    def dispatchcommand(self,origin,args,  text, match, event, func):
        kenni = self.wrapped(origin, text, match)
        input = self.input(origin, text, match, event, args)
        nick = (input.nick).lower()
        # blocking ability
        if os.path.isfile("blocks"):
            g = open("blocks", "r")
            contents = g.readlines()
            g.close()

            try:
                bad_masks = contents[0].split(',')
            except:
                bad_masks = ['']

            try:
                bad_nicks = contents[1].split(',')
            except:
                bad_nicks = ['']

            try:
                bad_idents = contents[2].split(',')
            except:
                bad_idents = ['']

            # check for blocked hostmasks
            if len(bad_masks) > 0:
                host = origin.host
                host = host.lower()
                for hostmask in bad_masks:
                    hostmask = hostmask.replace("\n", "").strip()
                    if len(hostmask) < 1: continue
                    try:
                        re_temp = re.compile(hostmask)
                        if re_temp.findall(host):
                            return
                    except:
                        if hostmask in host:
                            return
            # check for blocked nicks
            if len(bad_nicks) > 0:
                for nick in bad_nicks:
                    nick = nick.replace("\n", "").strip()
                    if len(nick) < 1: continue
                    try:
                        re_temp = re.compile(nick)
                        if re_temp.findall(input.nick):
                            return
                    except:
                        if nick in input.nick:
                            return

            if len(bad_idents) > 0:
                for ident in bad_idents:
                    ident = ident.replace('\n', '').strip()
                    if len(ident) < 1: continue
                    try:
                        re_temp = re.compile(ident)
                        if re_temp.findall(input.ident):
                            return
                    except:
                        if ident in input.ident:
                            return

        # stats
        if func.thread:
            targs = (func, origin, kenni, input)
            t = threading.Thread(target=self.call, args=targs)
            t.start()
        else:
            self.call(func, origin, kenni, input)

        for source in [origin.sender, origin.nick]:
            try:
                self.stats[(func.name, source)] += 1
            except KeyError:
                self.stats[(func.name, source)] = 1

    def dispatch(self, origin, args):
        text, event, args = args[0], args[1], args[2:]
        #print(text)
        #self.msg(self.logchan_pm,  text, True)
        for priority in ('high', 'medium', 'low'):
            items = list(self.rules[priority].items())
            for regexp, funcs in items:
                for func in funcs:
                    if event != func.event: continue
                    match = regexp.match(text)
                    if match:
                        self.dispatchcommand(origin,args, text, match, event, func)

            items = list(self.commands[priority].items())
            for command, funcs in items:
                for func in funcs:
                    if event != func.event: continue
                    prefix = self.config.prefix
                    if hasattr(self.config, 'prefixes'):
                        if origin.sender in self.config.prefixes:
                            prefix = self.config.prefixes[origin.sender]
                    template = r'(?i)^%s(%s)(?: +(.*))?$'
                    pattern = template % (prefix, command)
                    command = re.compile(pattern)
                    match = command.match(text)
                    if match:
                        self.dispatchcommand(origin,args, text, match, event, func)
            items = list(self.commandrules[priority].items())
            for commandrule, funcs in items:
                for func in funcs:
                    if event != func.event: continue
                    if hasattr(self.config, 'prefixes'):
                        prefix = self.config.prefix
                        if origin.sender in self.config.prefixes:
                            prefix = self.config.prefixes[origin.sender]
                    commandrule = re.compile(prefix + commandrule)
                    match = commandrule.match(text)
                    if match:
                        self.dispatchcommand(origin,args, text, match, event, func)


if __name__ == '__main__':
    print(__doc__)

