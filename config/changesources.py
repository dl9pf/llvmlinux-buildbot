from buildbot.changes.gitpoller import GitPoller
from llvmlinux.buildbot.changes.llvmpoller import LLVMPoller

import config
mastertype = config.defaults.get('defaults', "type")

pollers=config.pollers.sections()

def get_changesources():
    cs = []
    for poller in pollers:
	# restrict all but bot to basics
	if mastertype != '"llvmlinux-bot"' and not poller in ["llvm", "clang", "llvmlinux", "mainline"]:
	    continue
	# type first
	pollertype=config.pollers.get(poller, "type")
	if config.pollers.get(poller, "enabled"):
	    if pollertype.__contains__("git"):
		cs.append(GitPoller(
		    config.pollers.get(poller, "url"),
		    workdir='%s-poll' % poller,
		    branch=config.pollers.get(poller, "branch"),
		    pollinterval=int(config.pollers.get(poller, "pollinterval")),
		    project="%s" % poller
		))
    return cs

