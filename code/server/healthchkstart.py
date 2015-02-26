import sys,time, os

from nodemgr.nodemgr.healthcheck import RunningCheck
from nodemgr.nodemgr.nodemap import get_instance
from taskhandler import handle_tasks, health_check_report

from supernode import member_node_check

if (len(sys.argv) <2):
    print "Usage:  python", sys.argv[0], "<node-map-file>"
    exit


nodemap_instance = get_instance()

nodemap_instance.load_map(sys.argv[1])


PERIOD = 5

localhostname = os.uname()[1]




while True:

    time.sleep(PERIOD)
    
    handle_tasks(nodemap_instance)
    nodemap_instance.write_back()

    time.sleep(PERIOD)


    tarr = []

# refac0ir with urls.py block


    

#    for n in nodemap_instance.get_member_nodes():
#    print len(tarr),  " threads"

    member_node_check(nodemap_instance)

    
    handle_tasks(nodemap_instance)


    
    nodemap_instance.write_back()

