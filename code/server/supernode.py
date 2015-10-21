import os, json


from threading import Thread

from nodemgr.nodemgr.healthcheck import RunningCheck
from httplib import HTTPConnection, HTTPException
from nodemgr.nodemgr.simplequeue import write_task

from nodemgr.nodemgr.site_profile import gen_reg_xml, REG_FN

import pdb

import logging

PORT = int(os.environ.get("ESGF_NM_PORT"))


class NMapSender(Thread):

    def __init__(self,nmap, nn, ts=0):
        super(NMapSender, self).__init__()
        self.nodemap = nmap.nodemap
        self.target = nn
        self.ts = ts
        self.fromnode = nmap.myid
        self.logger = logging.getLogger("esgf_nodemanager")

    def run(self):

        conn = HTTPConnection(self.target, PORT, timeout=30)

        print self.target, PORT 

        tstr = ""

        if self.ts>0:
            tstr = "&timestamp=" + str(self.ts)
        

        try:
            conn.request("GET", "/esgf-nm-api?action=node_map_update" + tstr + "&from=" + self.fromnode , json.dumps(self.nodemap) )
            resp = conn.getresponse()
            if resp.status == 500:
                self.logger.error(resp.read())

        except Exception as e:
            print "Connection problem: " + str(e)


        conn.close()



class SNInitSender(Thread):

    def __init__(self, nn, ts, nmap):
        super(SNInitSender, self).__init__()

        self.target = nn
        self.ts = ts
        self.fromnode = nmap.myid
        self.logger = logging.getLogger("esgf_nodemanager")

    def run(self):

        print self.target, PORT 

        conn = HTTPConnection(self.target, PORT, timeout=30)


        tstr = "&timestamp=" + str(self.ts)

        try:
            conn.request("GET", "/esgf-nm-api?action=sn_init" + tstr + "&from=" + self.fromnode)
            resp = conn.getresponse()
            if resp.status == 500:
                self.logger.error(resp.read())


        except Exception as e:
            print "Connection problem: " + str(e)

        conn.close()

class NMRepoSender(Thread):

    def __init__(self, nn, task_d, nmap, ts):
        super(NMRepoSender, self).__init__()

        self.target = nn
        self.task_d = task_d
        self.fromnode = nmap.myid
        self.ts = ts
        self.logger = logging.getLogger("esgf_nodemanager")    

    def get_url_str(self):
        
        parts = ["application", "project", "name", "send"]

        arr = []
        for n in parts:
            arr.append("&")
            arr.append(n)
            arr.append("=")
            arr.append(self.task_d[n])
        
        return ''.join(arr)
        

    def run(self):


        print self.target, PORT 
        conn = HTTPConnection(self.target, PORT, timeout=30)


        tstr = "&timestamp=" + str(self.ts)

        try:
            conn.request("GET", "/esgf-nm-api?action=nm_repo_update" + tstr + "&from=" + self.fromnode + get_url_str(), json.dumps(self.task_d["update"]) )
            resp = conn.getresponse()
            if resp.status == 500:
                self.logger.error(resp.read())


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

    if len(mem) == 0:
        print "No nodes to reassign"
        return True

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

    for n in nm_inst["membernodes"]:


        if n["supernode"] == sn_id:

            if n["status"] == "OK":
                return
            

            n["status"] = "OK"
        else:
            for x in n["members"]:
                
                if "temp_assign" in x and x["temp_assign"] and x["prev_owner"] == sn_id:
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


def check_properties(nodemap_instance):


    tmp_props = []


    for n in nodemap_instance.nodemap["supernodes"]:


        if n[hostname] != localhostname and n["health"] == "good":
            
            target = n[hostname]

            conn = HTTPConnection(target, PORT, timeout=30)    
            conn.request("GET", "/esgf-nm-api/node-props.json" )
            resp = conn.getresponse()


            if resp.status == 200:
                dat = resp.read()
                
                obj = json.loads(dat)

                # TODO: Are we producing duplicate entries?
                for n in obj:

                    val = obj[n]
                    tmp_props.append(val)

            else:
                # TODO: log these sorts of errors
                print "An Error has occurred"
                print resp.read()
    for n in nodemap_instance.prop_store:
        val = nodemap_instance.prop_store[n]

        tmp_props.append(n)
    
    out_xml = gen_reg_xml(tmp_props)
        
    f = open(REG_FN, 'w')
    f.write(out_xml)
    f.close()

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


def send_repo_upd_to_others(task_d, nmap):

    # get supernodes -  omit project for now
    nodes = nmap.get_supernode_list()


    clond = task_d.copy()

    clond["send"] = False

    # but get the project here
    
   
    if (nodes is None) or len(nodes) == 0:
        return 

    tarr = []

    for nn in nodes:
        if nn != nmap.myname:

            nms = NMRepoSender(task_d, nn, ts)

            nms.start()
            tarr.append(nms)

    nodes = nmap.get_member_nodes(task_d["project"])    

    for nn in nodes:

        nms = NMRepoSender(task_d, nn, ts)

        nms.start()
        tarr.append(nms)


    for t in tarr:
        t.join()
        return

    


def supernode_init(nmap, ts):

    nodes = nmap.get_supernode_list()

    tarr = []

    for nn in nodes:
        if nn != nmap.myname:

            inits = SNInitSender(nn, ts, nmap)

            inits.start()
            tarr.append(inits)

    for t in tarr:
        t.join()
    

def my_turn(time_delta,  sn_id, total_sn, total_period):



    mod_delta = time_delta % ( total_sn * total_period)

#    print "turn check:", mod_delta, sn_id, total_period
    
    if ( mod_delta  >= (sn_id -1) * total_period and mod_delta <  sn_id * total_period): 
        return True
    else:
        return False
        
def calc_time(curr, start, q, sl):

    return int((( curr - start) / sl ) % q)


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
            
                    
