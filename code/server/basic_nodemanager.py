import sys
from time import sleep

from supernode import member_node_check()

from nodemgr.nodemgr.nodemap import get_instance
from taskhandler import handle_tasks

if (len(sys.argv) <2):
    print "Usage:  python", sys.argv[0], "<node-map-file>"
    exit

nodemap_instance = get_instance()

nodemap_instance.load_map(sys.argv[1])

while (True):

    sleep(5)

    handle_tasks(nodemap_instance)

    sleep(5)

