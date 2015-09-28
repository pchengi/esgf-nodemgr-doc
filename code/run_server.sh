#echo make sure you have python2.7 + django in your environment


if [ -z $ESGF_NM_TASKS ]; then
    echo please set ESGF_NM_TASKS to a directory for temporary task storage
    exit 1
fi

rm $ESGF_NM_TASKS/*

if [ -z $ESGF_NODEMGR_MAP ] ; then
    echo please set ESGF_NODEMGR_MAP to your node map file
    exit 1
fi

if [ -z $ESGF_NM_PORT ] ; then
    echo please set ESGF_NM_PORT
    exit 1
fi



python server/basic_nodemanager.py $ESGF_NODEMGR_MAP $ESGF_NM_TIMESTAMP &
python server/nodemgr/manage.py runserver 0.0.0.0:$ESGF_NM_PORT
kill %1