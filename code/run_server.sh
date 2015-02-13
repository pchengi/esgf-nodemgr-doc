rm /export/ames4/tasks/*
python server/basic_nodemanager.py node_mgr_map.json &
server/nodemgr/manage.py runserver 0.0.0.0:80
kill %1