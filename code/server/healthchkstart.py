from nodemgr.nodemgr.healthcheck import get_node_list, RunningCheck

import sys,time, os


PERIOD = 10

localhostname = os.uname()[1]


while True:

    time.sleep(PERIOD)

    
    tarr = []

# refac0ir with urls.py block
    for n in get_node_list():


        if n != localhostname:
            t = RunningCheck(n, True)
            t.start()
            tarr.append(t)


#    print len(tarr),  " threads"


    for tt in tarr:

            tt.join()
            print tt.nodename, tt.eltime
            # ADD to edge map (TODO) 
