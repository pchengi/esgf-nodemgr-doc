from simplequeue import write_task


from django.http import HttpResponse


def nodemgrapi(request):


    resp_code="OK"

    qd = request.GET

    action = qd["action"]

    if action == "add_member":

        json = json.dumps(qd)

        write_task(qd)
    else:
        resp_code = "INVALID_REQ"

    return HttpResponse(resp_code)

