#!/usr/bin/env python3
import os, sys
from importlib.machinery import SourceFileLoader

class Configs():
    def __init__(self, config_paths):
        self.config_paths = config_paths

    def load_modules(self, config_modules):
        for config_name in self.config_paths:
            name = os.path.basename(config_name).split('.')[0] + '_config'
            module = SourceFileLoader(name, config_name).load_module()
            module.filename = config_name

            if not hasattr(module, 'prefix'):
                module.prefix = r'\.'

            if not hasattr(module, 'name'):
                module.name = 'Kenni: https://github.com/jztech101/kenni/'

            if not hasattr(module, 'port'):
                module.port = 6667

            if not hasattr(module, 'password'):
                module.password = None

            if not hasattr(module, 'ssl'):
                module.ssl = False

            if module.host == 'irc.example.net':
                error = ('Error: you must edit the config file first!\n' +
                            "You're currently using %s" % module.filename)
                print(error, file=sys.stderr)
                sys.exit(1)

            config_modules.append(module)

