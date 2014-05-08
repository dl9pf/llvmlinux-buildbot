# Load local options.
import os
import ConfigParser

passwords = ConfigParser.RawConfigParser()
passwords.read(os.path.join(os.path.dirname(__file__), 'passwords.cfg'))
defaults = ConfigParser.RawConfigParser()
defaults.read(os.path.join(os.path.dirname(__file__), 'defaults.cfg'))
pollers = ConfigParser.RawConfigParser()
pollers.read(os.path.join(os.path.dirname(__file__), 'pollers.cfg'))

import slaves
import changesources

