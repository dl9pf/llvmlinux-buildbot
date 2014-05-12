import config
from buildbot.config import BuilderConfig
mastertype = config.defaults.get('defaults', "type")
#builders = config.builderlist.sections()

from buildbot.process.factory import BuildFactory
from buildbot.steps.source.git import Git

from buildbot.steps.shell import ShellCommand



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
    defaultslaves.append("vm-builder")

    afactory = BuildFactory()
    afactory.addStep(Git(repourl='http://git.linuxfoundation.org/llvmlinux.git', 
			      mode='incremental',
			      alwaysUseLatest=True,
			      logEnviron=False,
			      clobberOnFailure=True))
    for i in TF.get_steps("vexpress", llvmclang="", runtest=1, runhwtest=0):
	afactory.addStep(i)
    afactory.addStep(ShellCommand(workdir="../", description="clone",
				    haltOnFailure=False,
				    logEnviron=False,
                                    command=["git", "clone", "1_llvmlinux/build/.git", "common"]))
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
    afactory.addStep(ShellCommand(workdir="../common/",
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
                             description='test-clang-boot-poweroff',
                             haltOnFailure=True,
			     logEnviron=False,
                             timeout=2400)
    ]
    
    # build factory for llvm builder
    factory_llvm = BuildFactory()
    factory_llvm.addStep(ShellCommand(workdir="../common/clang/src/llvm", command=["git", "remote", "-v", "update"],
                     description='gitup',
                     haltOnFailure=True,
                     logEnviron=False,
                     timeout=3600))
    factory_llvm.addStep(Git(repourl='http://llvm.org/git/llvm.git', 
                     mode='incremental',
                     clobberOnFailure=True,
		     logEnviron=False,
                     workdir="../common/toolchain/clang/src/llvm"))
    factory_llvm.addStep(ShellCommand(workdir="../common", command=["make", "-C", "targets/vexpress", "GIT_HARD_RESET=1", "llvm-clean"],
                     description='llvm-clean',
                     haltOnFailure=True,
                     logEnviron=False,
                     timeout=3600))
    factory_llvm.addSteps(common_commands)
    
    # build factory for clang builder
    factory_clang = BuildFactory()
    factory_clang.addStep(ShellCommand(workdir="../common/clang/src/clang", command=["git", "remote", "-v", "update"],
                     description='gitup',
                     haltOnFailure=True,
                     logEnviron=False,
                     timeout=3600))
    factory_clang.addStep(Git(repourl='http://llvm.org/git/clang.git', 
                     mode='incremental',
		     logEnviron=False,
                     clobberOnFailure=True,
                     workdir="../common/toolchain/clang/src/llvm/tools/clang"))
    factory_clang.addStep(ShellCommand(workdir="../common", command=["make", "-C", "targets/vexpress", "GIT_HARD_RESET=1", "clang-clean"],
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

    return bld
#    if mastertype == '"llvmlinux-bot"':
	# REMOTE BUILDERS
    #
