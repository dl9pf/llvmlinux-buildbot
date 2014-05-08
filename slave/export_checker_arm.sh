#!/bin/bash


cp -ar /home/buildbot/buildbot/sandbox/slave/common/targets/vexpress/tmp/scan-build-2*   /home/buildbot/buildbot/sandbox/master/public_html/checker/ || true
rm -rf /home/buildbot/buildbot/sandbox/slave/common/targets/vexpress/tmp/scan-build-2*

pushd /home/buildbot/buildbot/sandbox/master/public_html/checker/
all=`ls | grep scan-build-2`

stay=`ls | grep scan-build-2 | tail -n10`

if ! test x"$stay" == x"" ; then

    for i in $stay ; do export all=$(echo $all | sed -e "s#$i##g") ; done

    if ! test x"$all" == x""  ; then
	for i in $all ; do rm -rf $i ; done
    fi

    rm -rf scan-build-latest || true
    ln -sf `ls | grep scan-build-2 | tail -1` scan-build-latest || true

fi

popd