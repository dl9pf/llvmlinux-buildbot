from buildbot.changes.gitpoller import GitPoller
from llvmlinux.buildbot.changes.llvmpoller import LLVMPoller

"""
c['change_source'].append(LLVMPoller(projects=[
    "llvm",
    "cfe",
    "clang-tests-external",
    "clang-tools-extra",
    "polly",
    "compiler-rt",
    "lld",
    "lldb",
    "openmp"]))
GitPoller(
	        'http://git.linuxfoundation.org/llvmlinux.git',
	        workdir='llvmlinux-poller',
	        branch='master',
	        pollinterval=596, 
	        project='llvmlinux')
"""

import config
mastertype = config.defaults.get('defaults', "type")

pollers=config.pollers.sections()

def get_changesources():
    if mastertype == '"llvmlinux-bot"':
	cs = []

	for poller in pollers:
	    # type first
	    pollertype=config.pollers.get(poller, "type")
	    if config.pollers.get(poller, "enabled"):
		if pollertype.__contains__("git"):
		    cs.append(GitPoller(
			    config.pollers.get(poller, "url"),
			    workdir='%s-poll' % poller,
			    branch=config.pollers.get(poller, "branch"),
			    pollinterval=int(config.pollers.get(poller, "pollinterval")),
			    project='%s' % poller
			))
	return cs
    else:
	return [
	]

