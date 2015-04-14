import sys
from time import sleep, time

from supernode import member_node_check, supernode_check, links_check, supernode_init, my_turn

from nodemgr.nodemgr.nodemap import get_instance as nm_get_instance
from taskhandler import handle_tasks

from time_store import get_instance as ts_get_instance

if (len(sys.argv) <2):
    print "Usage:  python", sys.argv[0], "<node-map-file>"
    exit


nodemap_instance = nm_get_instance()

nodemap_instance.load_map(sys.argv[1])

timestore_instance = ts_get_instance()

timestore_instance.filename = sys.argv[2]

count = 0

QUANTA = 12

LINK_CHECK_TIME=6

SLEEP_TIME= 5

MasterNode = (nodemap_instance.myid == "1")

supernode_count = len(nodemap_instance.nodemap["supernodes"])


if MasterNode:

    timestore_instance.ts = int(time())
    supernode_init(nodemap_instance, timestore_instance.ts)

while (True):

    # this is the inital timestamp to be distributed to supernodes for determining when each performs its lead in the health check.  


        

    sleep(SLEEP_TIME)

    handle_tasks(nodemap_instance)

    
    
    if count == 0:
        cur_ts = time()
        

        if timestore_instance.ts > 0 and my_turn(cur_ts - timestore_instance.ts, int(nodemap_instance.myid), supernode_count, QUANTA * SLEEP_TIME ):
            supernode_check(nodemap_instance)

        if nodemap_instance.myid > -1:
            member_node_check(nodemap_instance)
    
    nodemap_instance.write_back()

    count = count + 1


    if count == LINK_CHECK_TIME:
        cur_ts = time()
        if timestore_instance.ts > 0 and my_turn(cur_ts - timestore_instance.ts, int(nodemap_instance.myid), supernode_count, QUANTA * SLEEP_TIME ):
            links_check(nodemap_instance)
            

    if count == QUANTA:
        count = 0
        supernode_count = len(nodemap_instance.nodemap["supernodes"])        
