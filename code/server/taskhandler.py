import json, os
from time import time
from nodemgr.nodemgr.simplequeue import get_next_task
from nodemgr.nodemgr.healthcheck import RunningCheck
hostname = os.uname()[1]

from supernode import send_map_to_others, NMapSender

def health_check_fwd(task_d, nmap):

    fromnode = task_d["from"]

#    tarr = []
        
    checkarr = []
    first = True
# Refactor with manager.py block
    for n in nmap.get_supernode_list():
            
            
        if (n != hostname and  n != fromnode ):

            t = RunningCheck(n, False, first, checkarr , fromnode)
            t.start()
            first = False
            #               tarr.append(t)  
 #   for t in tarr:
 #       t.join()


def health_check_report(task_d, nmap):

    from_node = task_d["from"]

    from_id = nmap.snidx[from_node]

    edgelist = nmap.nodemap["links"]

    for n in task_d.keys():

        if n != "from" and n != "action":
            
            speed = task_d[n]

            to_id = nmap.snidx[n]
            
            if (int (from_id) < int(to_id)): 

                for ee in edgelist:
                    if ee["from"] == from_id and ee["to"] == to_id:
                        if speed < 0:
                            ee["status"] = "down"
                        else:
                            ee["status"] = "up"
                        ee["speed"] = float(speed)
                        nmap.dirty = True
                        break
    

def node_map_update(task_d, nmap):
    new_map = task_d["update"]

    nmap.nodemap = json.loads(new_map)
    
    nmap.dirty = True
    send_map_to_others(True, nmap)
    

def add_member(task_d, nmap):

    ts = int(time())

    rc = nmap.assign_node(task_d["from"], task_d["project"], task_d["standby"] == "True")
    send_map_to_others(False, nmap)




def remove_member(task_d, nmap):
    print task_d["from"]
    if nmap.remove_member(task_d["from"]):
        print "removed"
    else:
        print "not removed"

def handle_tasks(nmap):

    task = get_next_task()

    while (len(task) > 0):
        
        task_d = json.loads(task)

        action = task_d["action"]

        eval(action)(task_d, nmap)
        
        task = get_next_task()