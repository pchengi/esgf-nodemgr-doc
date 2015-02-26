import sys
from time import sleep

from supernode import member_node_check, supernode_check, links_check

from nodemgr.nodemgr.nodemap import get_instance
from taskhandler import handle_tasks

if (len(sys.argv) <2):
    print "Usage:  python", sys.argv[0], "<node-map-file>"
    exit



nodemap_instance = get_instance()

nodemap_instance.load_map(sys.argv[1])

count = 0

QUANTA = 12

MasterNode = (nodemap_instance.myid == "1")


while (True):

    sleep(5)

    handle_tasks(nodemap_instance)

    
    if count == 0:
        if MasterNode:
            supernode_check(nodemap_instance)

        if nodemap_instance.myid > -1:
            member_node_check(nodemap_instance)
    
    nodemap_instance.write_back()

    count = count + 1

    if count == 4:
        if MasterNode:
            links_check(nodemap_instance)
            

    if count == QUANTA:
        count = 0
