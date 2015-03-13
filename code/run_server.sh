#echo make sure you have python2.7 + django in your environment
rm /export/ames4/tasks/*
python server/basic_nodemanager.py $ESGF_NODEMRG_MAP &
server/nodemgr/manage.py runserver 0.0.0.0:80
kill %1