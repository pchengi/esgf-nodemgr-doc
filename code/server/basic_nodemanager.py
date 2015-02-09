import sys
from time import sleep


from nodemgr.nodemgr.nodemap import NodeMap
from taskhandler import handle_tasks

if (len(sys.argv) <2):
    print "Usage:  python", sys.argv[0], "<node-map-file>"
    exit

nodemap_instance = NodeMap(sys.argv[1])

while (True):

    sleep(5)

    handle_tasks(nodemap_instance)
