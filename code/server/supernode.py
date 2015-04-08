import os, json


from threading import Thread

from nodemgr.nodemgr.healthcheck import RunningCheck
from httplib import HTTPConnection, HTTPException
from nodemgr.nodemgr.simplequeue import write_task

import pdb

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

        

        try:
            conn.request("GET", "/esgf-nm-api?action=node_map_update" + tstr + "&from=" + self.fromnode , json.dumps(self.nodemap) )
            resp = conn.getresponse()
            if resp.status == 500:
                print resp.read()

        except Exception as e:
            print "Connection problem: " + str(e)


        conn.close()


localhostname = os.uname()[1]

def node_redist(nm_inst, sn_id):


#    pdb.set_trace()

    MAX_PER_SN = 3

# Find entry for down node
    
    free_slots = []

    for n in nm_inst["membernodes"]:

        if n["supernode"] == sn_id:


            x = n
        else:
            if len(n["members"]) < MAX_PER_SN:
                free_slots.append([n, MAX_PER_SN - len(n["members"])])
            

    x["status"] = "reassigned"  
        
    idx = 0

    mem = x["members"]

    summ = 0
    for z in free_slots:
        summ+=z[1]

# need to promote a member node if nothing available
    if summ < len(mem):
        return False
        
    for z in free_slots:

        for i in range(z[1]):

            cl = mem[idx].copy()
            
            cl["temp_assign"] = True
            cl["prev_owner"] = sn_id

            print z

            z[0]["members"].append(cl)
            
            idx=idx+1
            if idx == len(mem):
                return True


def node_return(nm_inst, sn_id):

    for n in nm_inst["members"]:


        if n["supernode"] == sn_id:

            if n["status"] == "OK":
                return
            

            n["status"] = "OK"
        else:
            for x in n["members"]:
                if x["temp_assign"] and x["prev_owner"] == sn_id:
                    n["members"].remove(x)





                


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

#    pdb.set_trace()

    changed = False
    
    snodes = nmap.nodemap["supernodes"]

    new_down = []

    new_back_up = []
    
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

            new_down.append(snodes[i]["id"])

#            print "  changed bad"
        elif (not down) and snodes[i]["health"] == "unreachable":
            snodes[i]["health"] = "good"
            changed = True
#            print "  change to good"
            new_back_up.append(snodes[i]["id"])

    if changed:
        nmap.dirty = True

        
        i =0

#        need_to promote 
        for sn_id in new_down:

            print "Supernode down and dealing with it", sn_id
            if (not node_redist(nmap.nodemap, sn_id)):

                for id2 in new_down[i:]:
                    promote_members(nmap, id2)
                break
            i = i + 1


        for sn_id in new_back_up:
            node_return(nmap.nodemap, sn_id)


        send_map_to_others(False, nmap)
        send_map_to_others(True, nmap)
            
                    
