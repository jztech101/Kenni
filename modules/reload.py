#!/usr/bin/env python3
import sys, os.path, time, imp
import irc

def f_reload(kenni, input):
    """Reloads a module, for use by admins only."""
    if not input.admin: return

    name = input.group(2)
    if name == kenni.config.owner:
        return kenni.say('What?')

    if (not name) or (name == '*'):
        kenni.variables = None
        kenni.commands = None
        kenni.setup()
        return kenni.say('done')

    if name not in sys.modules:
        return kenni.say('%s: no such module!' % name)

    # Thanks to moot for prodding me on this
    path = sys.modules[name].__file__
    if path.endswith('.pyc') or path.endswith('.pyo'):
        path = path[:-1]
    if not os.path.isfile(path):
        return kenni.say('Found %s, but not the source file' % name)

    module = imp.load_source(name, path)
    sys.modules[name] = module
    if hasattr(module, 'setup'):
        module.setup(kenni)

    mtime = os.path.getmtime(module.__file__)
    modified = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(mtime))

    kenni.register(vars(module))
    kenni.bind_commands()

    kenni.say('%r (version: %s)' % (module, modified))
    if hasattr(kenni.config, 'logchan_pm'):
        if not input.owner:
            kenni.msg(kenni.config.logchan_pm, 'RELOADED: %r -- (%s, %s) - %s' % (module, input.sender, input.nick, modified))
f_reload.commands = ['reload']
f_reload.rule = ('$nick', ['reload'], r'(\S+)?')
f_reload.priority = 'low'
f_reload.thread = False

if __name__ == '__main__':
    print(__doc__.strip())
