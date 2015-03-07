from simplequeue import RunningWrite


from django.http import HttpResponse
import json

import pdb

def nodemgrapi(request):
    
#    print "API request"

#    pdb.set_trace()

    resp_code="OK"


    qd = request.GET

    action = qd["action"]
    
    task = ""

    if action in ["add_member", "remove_member"]:

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

    return HttpResponse(resp_code)
