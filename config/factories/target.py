#
import config.factories.targetsteps
import config.factories.targethwsteps

def get_steps(target, llvmclang="stable", runtest=1, runhwtest=0):
    f = []
    for i in config.factories.targetsteps.get_targetsteps(target, llvmclang, runtest):
	f.append(i)
    if not runhwtest==0:
        for i in config.factories.targethwsteps.get_targetsteps(target):
	    f.append(i)
    return f
