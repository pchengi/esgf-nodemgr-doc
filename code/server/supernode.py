import os, json

from threading import Thread

from nodemgr.nodemgr.healthcheck import RunningCheck
from httplib import HTTPConnection


class NMapSender(Thread):

    def __init__(self,nmap, nn):
        self.nodemap = nmap.nodemap
        self.target = nn
    def run():

        conn = HTTPConnection(self.target, 80, timeout=30)

        conn.request("POST", "/esgf-nm-api?action=update_map", json.dumps(self.nodemap) )
        foo = conn.getresponse()

        conn.close




def supernode_check(nodemap_instance):

    for n in nodemap_instance.get_supernode_list():


        if n != localhostname:
            t = RunningCheck(n, True)
            t.start()
            tarr.append(t)


    report_dict = {}

    report_dict["from"] = localhostname

    for tt in tarr:

        tt.join()

        report_dict[tt.nodename] = tt.eltime
    
    health_check_report(report_dict, nodemap_instance)


def send_map_to_others(members, nmap):
    
    nodes = []

    if members:
        nodes = nmap.get_member_nodes()
    else:
        nodes = nmap.get_supernode_list()


    if (not nodes is None) or len(nodes) == 0:
        return

    tarr = []

    for nn in nodes:
        if nn != nmap.myname:

            nms = NMapSender(nmap, nn)

            nms.start()
            tarr.append(nms)

    for t in tarr:
        t.join()



def member_node_check(nmap):

    nodes = nmap.get_member_nodes()

    if (not nodes is None) or len(nodes) == 0:
        return


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
        

    
