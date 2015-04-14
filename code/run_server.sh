#echo make sure you have python2.7 + django in your environment
rm $ESGF_NM_TASKS/*
python server/basic_nodemanager.py $ESGF_NODEMGR_MAP $ESGF_NM_TIMESTAMP &
server/nodemgr/manage.py runserver 0.0.0.0:80
kill %1