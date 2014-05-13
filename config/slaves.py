import buildbot
import buildbot.buildslave
import os

import config
mastertype = config.defaults.get('defaults', "type")

def create_slave(name, *args, **kwargs):
    if name == "localhost":
	password = name
    elif mastertype == '"llvmlinux-bot"':
        password = config.passwords.get('Slave Passwords', name)
    return buildbot.buildslave.BuildSlave(name, password=password, *args, **kwargs)

def get_build_slaves():
    if mastertype == '"llvmlinux-bot"':
	return [
	    # default slave on VM
	    create_slave("localhost", properties={'jobs': 2}, max_builds=1),
	    create_slave("vm-builder", properties={'jobs': 2}, max_builds=1),
	    # remote slaves
	    create_slave("target.vexpress", properties={'jobs': 4}, max_builds=1),
	    create_slave("target.x86_64", properties={'jobs': 4}, max_builds=1),
	    create_slave("target.beaglebone", properties={'jobs': 4}, max_builds=1),
	    create_slave("target.x86_64-linux-next", properties={'jobs': 4}, max_builds=1),
	    # more to be added below
	    # ...
            ]
    else:
	return [
	    create_slave("localhost", properties={'jobs': 2}, max_builds=1),
	]
