#echo make sure you have python2.7 + django in your environment


export ESGF_NM_PORT=6720
export NM_TEST_SRV=true
python server/basic_nodemanager.py &

python server/nodemgr/manage.py runserver 0.0.0.0:$ESGF_NM_PORT
kill %1
