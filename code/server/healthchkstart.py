import sys,time, os

from nodemgr.nodemgr.healthcheck import RunningCheck
from nodemgr.nodemgr.nodemap import NodeMap
from taskhandler import handle_tasks, health_check_report

if (len(sys.argv) <2):
    print "Usage:  python", sys.argv[0], "<node-map-file>"
    exit


nodemap_instance = NodeMap(sys.argv[1])


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






    report_dict = {}

    for tt in tarr:

            tt.join()

            if tt.fwdcheck:
                
                tt.nodename, tt.eltime

#    for n in nodemap_instance.get_member_nodes():
#    print len(tarr),  " threads"

    
    handle_tasks(nodemap_instance)
    
    nodemap_instance.write_back()

