import os

from nodemgr.nodemgr.healthcheck import RunningCheck


def member_node_check(nmap):

    nodes = nmap.get_member_nodes()

    tarr = []

    for nn in nodes:

        r= RunningCheck(nn, False, False)
        tarr.append(r)
        r.start()

#        print str(r), " started"
    
    for t in tarr:

        t.join()
        
 #       print str(t), "joined"
        status = "good"

        if t.eltime < 0:
            status = "unreachable"
   #     else:
    #        print "eltime " , eltime 
# For now we don't care about time to reach a member node - potential
# future optimization
        nmap.update_membernode_status(t.nodename, status)
        

    
