import sys
from time import sleep, time

from supernode import member_node_check, supernode_check, links_check, supernode_init, my_turn, calc_time

from nodemgr.nodemgr.nodemap import get_instance as nm_get_instance
from taskhandler import handle_tasks

from time_store import get_instance as ts_get_instance

def usage():
    print "Usage:  python", sys.argv[0], "<node-map-file> [timestamp-file if SN]"
    exit(1)
    

if (len(sys.argv) <2):
    usage()


nodemap_instance = nm_get_instance()

nodemap_instance.load_map(sys.argv[1])
supernode = False

if (nodemap_instance.myid > 0) :
    timestore_instance = ts_get_instance()
    if len(sys.argv) < 3:
        print "This node is running as a supernode; timestamp file parameter is missing"
        usage()
    
    timestore_instance.filename = sys.argv[2]
    supernode = True


count = 0

QUANTA = 12

HEALTH_CHECK_TIME=2
LINK_CHECK_TIME=5

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
    

    if (supernode):

        cur_ts = time()
        count = calc_time(cur_ts, timestore_instance.ts, QUANTA,  SLEEP_TIME) 
        
#        print "Count:" , count
    
        if count == HEALTH_CHECK_TIME:

        
            if timestore_instance.ts > 0 and my_turn(cur_ts - timestore_instance.ts, int(nodemap_instance.myid), supernode_count, QUANTA * SLEEP_TIME ):
                print "SN check", count, cur_ts
                supernode_check(nodemap_instance)

            if nodemap_instance.myid > -1:
                member_node_check(nodemap_instance)
    


        if count == LINK_CHECK_TIME:

            if timestore_instance.ts > 0 and my_turn(cur_ts - timestore_instance.ts, int(nodemap_instance.myid), supernode_count, QUANTA * SLEEP_TIME ):
                print "Status review", count, cur_ts
                links_check(nodemap_instance)
            

    nodemap_instance.write_back()            
    supernode_count = len(nodemap_instance.nodemap["supernodes"])        
