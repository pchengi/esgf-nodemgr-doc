import json, os
from time import time
from nodemgr.nodemgr.simplequeue import get_next_task
from nodemgr.nodemgr.healthcheck import RunningCheck
hostname = os.uname()[1]

from supernode import send_map_to_others

from time_store import get_instance

# for now not used
#from user_api import put_file

def task_set_status(task_d, nmap):

    print "Got the status message:", task_d["status"]


def task_node_properties(task_d, nmap):


    ky = task_d["esgf.host"]
    print "node properties task" + ky
    status = task_d["status"]
    nmap.set_prop(ky, task_d)


def task_health_check_fwd(task_d, nmap):

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


def task_health_check_report(task_d, nmap):

    from_node = task_d["from"]

    from_id = nmap.snidx[from_node]

    edgelist = nmap.nodemap["links"]

    

    for n in task_d.keys():

        if n != "from" and n != "action":
            
            speed = float(task_d[n])

            if not n in nmap.snidx:
                print n,"not found in list"
                print "TODO: fetch new master list and broadcast"
                continue

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
            elif (int (from_id) > int(to_id)):
                for ee in edgelist:
                    if ee["to"] == from_id and ee["from"] == to_id:
                        if speed < 0:
                            ee["status"] = "down"
                        else:
                            ee["status"] = "up"
                        ee["speed"] = float(speed)
                        nmap.dirty = True
                        break

def task_node_map_update(task_d, nmap):
    new_map = task_d["update"]

    nmap.nodemap = json.loads(new_map)
    
    nmap.dirty = True
    send_map_to_others(True, nmap)


def task_nm_repo_update(task_d, nmap):
    
    upd = task_d["update"]

    put_file(task_d["application"], task_d["project"], task_d["name"], upd)

    if task_d["send"]:
        
        send_repo_upd_to_others(task_d, nmap)


def task_add_member(task_d, nmap):

    ts = int(time())

    rc = nmap.assign_node(task_d["from"], task_d["project"], task_d["standby"] == "True")
    send_map_to_others(False, nmap)




def task_remove_member(task_d, nmap):
    print "From", task_d["from"]
    if nmap.remove_member(task_d["from"]):
        print "removed"
    else:
        print "not removed"


def task_sn_init(task_d, nmap):


    print "timestore update"

    ts_inst = get_instance()

    ts_inst.ts = int(task_d["timestamp"])

    ts_inst.write()


switch = { 
"task_set_status": task_set_status,
"task_node_properties": task_node_properties,
 "task_health_check_fwd": task_health_check_fwd,
 "task_health_check_report": task_health_check_report,
"task_node_map_update": task_node_map_update,
"task_nm_repo_update": task_nm_repo_update,
"task_add_member": task_add_member,
"task_remove_member": task_remove_member,
"task_sn_init": task_sn_init 
}


def handle_tasks(nmap):

    task = get_next_task()

    while (len(task) > 0):
        
        task_d = json.loads(task)

        action = task_d["action"]
# TODO - this needs to be hardened before outside deployment
        fn_ptr = switch["task_" +action]
        retval = fn_ptr (task_d, nmap)
        
        task = get_next_task()
