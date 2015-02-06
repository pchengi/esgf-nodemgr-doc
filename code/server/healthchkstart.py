import sys,time, os

from nodemgr.nodemgr.healthcheck import get_node_list, RunningCheck
from nodemgr.nodemgr.nodemap import NodeMap



nodemap_instance = NodeMap()


PERIOD = 10

localhostname = os.uname()[1]




while True:

    time.sleep(PERIOD)
    
    handle_tasks(nodemap_instance)


    tarr = []

# refac0ir with urls.py block
    for n in nodemap_instance.get_supernode_list():


        if n != localhostname:
            t = RunningCheck(n, True)
            t.start()
            tarr.append(t)



    for n in nodemap_instance.get_member_nodes():
#    print len(tarr),  " threads"


    for tt in tarr:

            tt.join()
            print tt.nodename, tt.eltime
            # ADD to edge map (TODO) 
    
    handle_tasks(nodemap_instance)
    
    nodemap_instance.write_back()

