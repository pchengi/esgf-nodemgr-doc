from simplequeue import RunningWrite


from django.http import HttpResponse
import json, os

#import pdb

from nodemap import get_instance

nodemap_instance = get_instance()

nodemap_instance.load_map(os.environ.get("ESGF_NODEMGR_MAP"))
nodemap_instance.set_ro()

def nodemgrapi(request):
    
#    print "API request"

#    pdb.set_trace()

    resp_code="OK"


    qd = request.GET

    action = qd["action"]
    
    task = ""

    if action == "get_node_map":
        
        nodemap_instance.reload()
        resp_code = nodemap_instance.get_indv_node_status_json()
        
    elif action in ["add_member", "remove_member"]:

        task = json.dumps(qd)


    elif action in ["node_map_update"]:

        print "update map!"

        data = request.body
        outd = qd.copy()
        outd["update"] = data

        task = json.dumps(outd)

    else:
        resp_code = "INVALID_REQ"

    if (len(task) > 0):
        rw = RunningWrite(task)
        rw.start()

    return HttpResponse(resp_code, content_type="text/plain")

