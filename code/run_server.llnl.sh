#!/bin/bash
source /opt/nfs/esgf/nm_django/bin/activate
source conf_examples/nm2.env

#export ESGF_NM_PORT=6720
#export NM_TEST_SRV=true

#echo make sure you have python2.7 + django in your environment



python server/basic_nodemanager.py $ESGF_NODEMGR_MAP $ESGF_NM_TIMESTAMP &
python server/nodemgr/manage.py runserver 0.0.0.0:$ESGF_NM_PORT
kill %1