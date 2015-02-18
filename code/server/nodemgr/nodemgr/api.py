from simplequeue import RunningWrite


from django.http import HttpResponse
import json

def nodemgrapi(request):


    resp_code="OK"

    qd = request.GET

    action = qd["action"]
    
    task = ""

    if action in ["add_member"]:

        task = json.dumps(qd)


    elif action in ["node_map_update"]:
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

