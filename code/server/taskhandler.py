import json



def handle_tasks(nmap):

    task = get_next_task()

    while (len(task) > 0):
        
        task_d = json.loads(task)

        if task_d["action"] == "add_member":
            
            rc = nmap.assign_node(task_d["from"], task_d["project"], task_d["standby"] == "True")
#            if (not rc):

        elif task_d["action"] == "node_map_upadate":
            new_map = task_d["update"]

            nmap.replace(new_map)



        task = get_next_task()
