import os, json

from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.http import HttpResponse #, QueryDict

from healthcheck import RunningCheck

from simplequeue import write_task
from nodemap import NodeMap, PROPS_FN
from api import nodemgrapi

from site_profile import get_prop_st, REG_FN

global served 
served = False

# TODO - need to 
#hostname = os.uname()[1]

#checkarr = []
#MAPFILE = "/export/ames4/node_mgr_map.json"

#nodemap_instance = NodeMap(MAPFILE)



def write_resp(full):

    global served

    if served and (not full):
        return "OK"
    else:
        served = True
        ret = get_prop_st()
        return json.dumps(ret)

def healthcheckreport(request):
    qd = request.GET

    outd = qd.copy()
    outd["action"] = "health_check_report"
    

    write_task(json.dumps(outd))

    return HttpResponse("")


def healthcheckack(request):
# TODO check timestamp and write resp when the prop file is more recent.

    qd = request.GET



    if ("forward" in qd and qd["forward"] == "True"):

        outd = qd.copy()

        outd["action"] = "health_check_fwd"
        write_task(json.dumps(outd))
        print "checking on others"        

    resp = write_resp(False)
    return HttpResponse(resp)
    

def get_json(request):
    
    resp = ""

    if os.path.isfile(PROPS_FN):
        f = open(PROPS_FN)
        resp = f.read()
        f.close()

    else:
        print "no file"
        resp = "NO_FILE"

    return HttpResponse(resp)

def get_reg_xml(request):
    f = open(REG_FN)
    
    resp = f.read()
    f.close()
    
    return HttpResponse(resp)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nodemgr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)
                       url(r'^health-check-api', healthcheckack),
                       url(r'^health-check-rep', healthcheckreport),
                       url(r'^esgf-nm-api', nodemgrapi),
                       url(r'^esgf-nm/node-props.json', get_json),
                       url(r'^esgf-node-manager/registration.xml', get_reg_xml))

