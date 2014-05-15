import config
from buildbot.config import BuilderConfig
mastertype = config.defaults.get('defaults', "type")
#builders = config.builderlist.sections()

from buildbot.process.factory import BuildFactory
from buildbot.steps.source.git import Git

from buildbot.steps.shell import ShellCommand

from buildbot.steps.transfer import FileUpload


import config.factories.target as TF


# TODO - SPLIT into modules


def get_builders():
    bld = []
    # extract all slavenames 
#    slaves = config.slaves.get_build_slaves()
#    slavenames = []
#    for i in slaves:
#	slavenames.append(i.slavename)
    defaultslaves=[]
    defaultslaves.append("localhost")
    if mastertype == '"llvmlinux-bot"':
    	defaultslaves.append("vm-builder")

    bfactory = BuildFactory()
    bfactory.addStep(ShellCommand(workdir="./",
				haltOnFailure=False,
				command="if test ! -d build ; then git clone http://git.linuxfoundation.org/llvmlinux.git build; fi",
				description="checkout"))
    bfactory.addStep(ShellCommand(workdir="./build/",
				haltOnFailure=False,
				command="git pull",
				description="update"))
    bfactory.addStep(ShellCommand(workdir="./build/targets/x86_64-linux-next",
				haltOnFailure=False,
				command="make sync-all",
				description="checkout2"))
    bfactory.addStep(Git(repourl='git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git', 
			      mode='incremental',
			      alwaysUseLatest=True,
			      logEnviron=False,
			      workdir="./build/targets/x86_64-linux-next/src/linux"))
    for i in TF.get_steps("x86_64-linux-next", llvmclang="stable", runtest=1, runhwtest=0):
	bfactory.addStep(i)
    if mastertype == '"llvmlinux-bot"':
	bld.append(
		BuilderConfig(name="4_linux-next",
		slavenames=["target.x86_64-linux-next"],
		factory=bfactory))

    afactory = BuildFactory()
    afactory.addStep(Git(repourl='http://git.linuxfoundation.org/llvmlinux.git', 
			      mode='incremental',
			      alwaysUseLatest=True,
			      logEnviron=False,
			      clobberOnFailure=True))
    for i in TF.get_steps("vexpress", llvmclang="", runtest=1, runhwtest=0):
	afactory.addStep(i)
    afactory.addStep(ShellCommand(workdir="../",
				haltOnFailure=False,
				command="if test ! -d common ; then git clone 1_llvmlinux/build/.git common; fi",
				description="checkout"))
    afactory.addStep(ShellCommand(workdir="../common/",
                              haltOnFailure=True,
			      logEnviron=False,
                              command=["git", "remote", "-v", "update"],
                              description="update common"))
    afactory.addStep(ShellCommand(workdir="../common/",
                              haltOnFailure=True,
			      logEnviron=False,
                              command=["git", "pull"],
                              description=["pull", "update"]))
    afactory.addStep(ShellCommand(workdir="../common/targets/vexpress",
                              haltOnFailure=True,
			      logEnviron=False,
                              command=["make", "kernel-sync", "llvm-sync", "clang-sync"],
                              description="sync common"))
    bld.append(
      BuilderConfig(name="1_llvmlinux",
      slavenames=defaultslaves,
      factory=afactory))

    common_commands = [
         ShellCommand(workdir="../common", command=["make", "-C", "targets/vexpress", "GIT_HARD_RESET=1", "kernel-sync"],
                             description='kernel-clean',
                             haltOnFailure=True,
			     logEnviron=False,
                             timeout=2400)  ,
         ShellCommand(workdir="../common", command=["make", "-C", "targets/vexpress", "GIT_HARD_RESET=1", "test-boot-poweroff"],
                             description='clang-boot-poweroff',
                             haltOnFailure=True,
			     logEnviron=False,
                             timeout=2400),
#         ShellCommand(workdir="../common", command=["make", "-C", "targets/x86_64", "CONFIG=", "GIT_HARD_RESET=1", "kernel-sync"],
#                             description='kernel-clean',
#                             haltOnFailure=True,
#			     logEnviron=False,
#                             timeout=2400)  ,
#         ShellCommand(workdir="../common", command=["make", "-C", "targets/x86_64", "GIT_HARD_RESET=1", "test-boot-poweroff"],
#                             description='test-clang-boot-poweroff',
#                             haltOnFailure=True,
#			     logEnviron=False,
#                             timeout=2400),
	ShellCommand(workdir="../common/targets/vexpress", 
		     command="make llvm-settings | tee toolchain.cfg",
                     description='export stable toolchain',
                     haltOnFailure=False,
		     logEnviron=False,
                     timeout=2400),
	FileUpload(slavesrc="../common/targets/vexpress/toolchain.cfg",
                          masterdest="public_html/toolchain.cfg")
    ]
    
    # build factory for llvm builder
    factory_llvm = BuildFactory()
    factory_llvm.addStep(ShellCommand(workdir="../common/toolchain/clang/src/llvm", command=["git", "remote", "-v", "update"],
                     description='gitup',
                     haltOnFailure=True,
                     logEnviron=False,
                     timeout=3600))
    factory_llvm.addStep(Git(repourl='http://llvm.org/git/llvm.git', 
                     mode='incremental',
                     clobberOnFailure=True,
		     logEnviron=False,
                     workdir="../common/toolchain/clang/src/llvm"))
    factory_llvm.addStep(ShellCommand(workdir="../common", command=["make", "-C", "targets/vexpress", "llvm-clean"],
                     description='llvm-clean',
                     haltOnFailure=True,
                     logEnviron=False,
                     timeout=3600))
    factory_llvm.addSteps(common_commands)
    
    # build factory for clang builder
    factory_clang = BuildFactory()
    factory_clang.addStep(ShellCommand(workdir="../common/toolchain/clang/src/clang", command=["git", "remote", "-v", "update"],
                     description='gitup',
                     haltOnFailure=True,
                     logEnviron=False,
                     timeout=3600))
    factory_clang.addStep(Git(repourl='http://llvm.org/git/clang.git', 
                     mode='incremental',
		     logEnviron=False,
                     clobberOnFailure=True,
                     workdir="../common/toolchain/clang/src/clang"))
    factory_clang.addStep(ShellCommand(workdir="../common", command=["make", "-C", "targets/vexpress", "clang-clean"],
                     description='clang-clean',
                     haltOnFailure=True,
                     logEnviron=False,
                     timeout=3600))
    factory_clang.addSteps(common_commands)

    bld.append(
      BuilderConfig(name="2_llvm",
      slavenames=defaultslaves,
      factory=factory_llvm))

    bld.append(
      BuilderConfig(name="3_clang",
      slavenames=defaultslaves,
      factory=factory_clang))
    
    ### resetup Factories
    factory_resetup_common = BuildFactory()
    factory_resetup_common.addStep(ShellCommand(workdir="../",
                                            description="rm",
					    logEnviron=False,
                                            command=["rm", "-rRf", "common"]))
    factory_resetup_common.addStep(ShellCommand(workdir="../", description="clone",
					    logEnviron=False,
                                            command=["git", "clone", "1_llvmlinux/build/.git", "common"]))
    factory_resetup_common.addStep(ShellCommand(workdir="../common",
					    logEnviron=False,
                                            timeout=3600,
                                            description="refetch",
                                            command=["make", "-C", "targets/vexpress", "clang-fetch", "qemu-fetch", "kernel-fetch"]))

    bld.append(
	BuilderConfig(name="0_resetup",
	slavenames=defaultslaves,
	factory=factory_resetup_common))
    return bld
#    if mastertype == '"llvmlinux-bot"':
	# REMOTE BUILDERS
    #

