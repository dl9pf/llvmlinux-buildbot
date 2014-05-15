import urllib2
from buildbot.steps.shell import ShellCommand

def get_targetsteps(target, llvmclang="", runtest=1):
    steps=[]
    TARGET="targets/%s" % target
    TARGET.strip('"')
    steps.append(ShellCommand(command=["make", "llvm-sync", "clang-sync"],
			      description='llvm/clang-sync',
			      haltOnFailure=False,
			      logEnviron=False,
			      timeout=2400))
    cmd=["make", "-C", TARGET, "sync-all"]
    if llvmclang=="stable":
	CONFIGADD=""
	steps.append(ShellCommand(command="wget -O %s/toolchain.cfg http://buildbot.llvm.linuxfoundation.org/toolchain.cfg",
			      description='toolchain.cfg',
			      haltOnFailure=False,
			      logEnviron=False,
			      timeout=2400))
	CONFIGADD="CONFIG=toolchain.cfg"
	CONFIGADD.strip('"')
	cmd=["make", "-C", TARGET, CONFIGADD, "sync-all"]
    steps.append(ShellCommand(command=cmd,
			      description='sync-all',
			      haltOnFailure=False,
			      logEnviron=False,
			      timeout=2400))
    steps.append(ShellCommand(command=["make", "-C" , TARGET, "mrproper"],
			      description='mrproper',
			      haltOnFailure=True,
			      logEnviron=False,
			      timeout=2400))
    steps.append(ShellCommand(command=["make", "-C" , TARGET],
			      description='make',
			      haltOnFailure=True,
			      logEnviron=True,
			      timeout=3600))
    if runtest==1:
        steps.append(ShellCommand(command=["make", "-C" , TARGET , "test-boot-poweroff"],
			      timeout=2400,
			      description='test-boot',
			      haltOnFailure=True,
			      logEnviron=False,
			      usePTY=True))
    return steps