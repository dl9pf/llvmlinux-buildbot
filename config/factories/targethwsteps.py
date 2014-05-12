from buildbot.steps.shell import ShellCommand
def get_targetsteps(target):
    TARGET="targets/%s" % target
    steps=[]
    steps.add(ShellCommand(command=["make", "-C" , TARGET , "test-hw-pre"],
	      timeout=2400,
	      description='test-hw-pre',
	      haltOnFailure=True,
	      logEnviron=False,
	      usePTY=True))
    steps.add(ShellCommand(command=["make", "-C" , TARGET , "test-hw-run"],
	      timeout=2400,
	      description='test-hw-run',
	      haltOnFailure=True,
	      logEnviron=False,
	      usePTY=True))
    steps.add(ShellCommand(command=["make", "-C" , TARGET , "test-hw-post"],
	      timeout=2400,
	      description='test-hw-post',
	      haltOnFailure=True,
	      logEnviron=False,
	      usePTY=True))
    return steps