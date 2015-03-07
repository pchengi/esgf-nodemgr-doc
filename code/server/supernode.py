import os, json


from threading import Thread

from nodemgr.nodemgr.healthcheck import RunningCheck
from httplib import HTTPConnection
from nodemgr.nodemgr.simplequeue import write_task

class NMapSender(Thread):

    def __init__(self,nmap, nn, ts=0):
        super(NMapSender, self).__init__()
        self.nodemap = nmap.nodemap
        self.target = nn
        self.ts = ts
        self.fromnode = nmap.myid
    

    def run(self):

        conn = HTTPConnection(self.target, 80, timeout=30)

        tstr = ""
        if self.ts>0:
            tstr = "&timestamp=" + str(self.ts)

        conn.request("GET", "/esgf-nm-api?action=node_map_update" + tstr + "&from=" + self.fromnode , json.dumps(self.nodemap) )
        foo = conn.getresponse()

        conn.close()


localhostname = os.uname()[1]

def supernode_check(nodemap_instance):

    tarr = []

    for n in nodemap_instance.get_supernode_list():


        if n != localhostname:
            t = RunningCheck(n, True)
            t.start()
            tarr.append(t)


    report_dict = {}

    report_dict["action"] = "health_check_report"
    report_dict["from"] = localhostname

    for tt in tarr:

        tt.join()

        report_dict[tt.nodename] = tt.eltime
    
    
    write_task(json.dumps(report_dict))
#    health_check_report(report_dict, nodemap_instance)


def send_map_to_others(members, nmap, ts=0):
    
    nodes = []

    if members:
        nodes = nmap.get_member_nodes()
    else:
        nodes = nmap.get_supernode_list()


    if (nodes is None) or len(nodes) == 0:
        return

    tarr = []

    for nn in nodes:
        if nn != nmap.myname:

            nms = NMapSender(nmap, nn, ts)

            nms.start()
            tarr.append(nms)

    for t in tarr:
        t.join()



def member_node_check(nmap):

    nodes = nmap.get_member_nodes()

    if (nodes is None) or len(nodes) == 0:
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
        if (nmap.update_membernode_status(t.nodename, status)):
            send_map_to_others(False, nmap)
            send_map_to_others(True, nmap)

        

def links_check(nmap):

#    print "Links Check"

    changed = False
    
    snodes = nmap.nodemap["supernodes"]

    for i in range(nmap.nodemap["total_supernodes"]):
        
        
        
        nid = str(i+1)

        if (nid == nmap.myid):
            snodes[i]["health"] = "good"
            continue

        print "check on", i

        for v in nmap.nodemap["links"]:
            
            down = True

            if (nid == v["from"] or nid == v["to"]) and (v["status"] != "down"):
                down = False
#                print " found an up link"
                break

        if down and snodes[i]["health"] != "unreachable":
            snodes[i]["health"] = "unreachable"
            changed = True
#            print "  changed bad"
        elif (not down) and snodes[i]["health"] == "unreachable":
            snodes[i]["health"] = "good"
            changed = True
#            print "  change to good"

    if changed:
        nmap.dirty = True
        send_map_to_others(False, nmap)
        send_map_to_others(True, nmap)
            
                    