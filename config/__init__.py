# Load local options.
import os
import ConfigParser

defaults = ConfigParser.RawConfigParser()
defaults.read(os.path.join(os.path.dirname(__file__), 'defaults.cfg'))
pollers = ConfigParser.RawConfigParser()
pollers.read(os.path.join(os.path.dirname(__file__), 'pollers.cfg'))

mastertype = config.defaults.get('defaults', "type")
if mastertype == '"llvmlinux-bot"':
    passwords = ConfigParser.RawConfigParser()
    passwords.read(os.path.join(os.path.dirname(__file__), 'passwords.cfg'))

import slaves
import changesources
import builders

