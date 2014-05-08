
.PHONY: master slave

# MASTER
########
master-stop:
	@buildbot stop master

master-start:
	buildbot checkconfig master
	buildbot start master

master-restart: master-stop master-start

master-mrproper:
	( for i in $$(ls master/ | grep -v master.cfg | grep -v buildbot.tac) ; do rm -rf master/$$i ; done ) 
	buildbot upgrade-master master


# SLAVE
#######
slave-stop:
	@buildslave stop slave

slave-start:
	buildslave start slave

slave-restart: slave-stop slave-start

slave-mrproper:
	( for i in $$(ls slave/ | grep -v buildbot.tac | grep -v export* ) ; do rm -rf slave/$$i ; done ) 


