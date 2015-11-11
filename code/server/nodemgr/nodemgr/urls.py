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

MET_FN = os.environ.get("ESGF_NM_STATS_RES")


# TODO - need to 
#hostname = os.uname()[1]

#checkarr = []
#MAPFILE = "/export/ames4/node_mgr_map.json"

#nodemap_instance = NodeMap(MAPFILE)




def write_resp(full):

    global served

    met_resp = {}

    if os.path.isfile(MET_FN):
        f = open(MET_FN)
        met_in = f.read()
        try:
            met_resp = json.loads(met_in)
        except:
            print "JSON error with metrics file"
        f.close()

    if len(met_resp) > 0:
        met_resp["esgf.host"] = get_prop_st()["esgf.host"]
        met_resp["action"] = "node_properties"
        return 
    elif served and (not full):
        return "OK"
    else:
        print "first time, serving json"

        served = True
        ret = get_prop_st()
        ret.update(met_resp)
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


def get_metrics(request):
    
    resp = ""

    if os.path.isfile(MET_FN):
        f = open(MET_FN)
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
                       url(r'^esgf-nm/health-check-api', healthcheckack),
                       url(r'^esgf-nm/health-check-rep', healthcheckreport),
                       url(r'^esgf-nm/api', nodemgrapi),
                       url(r'^esgf-nm/node-props.json', get_json),
                       url(r'^esgf-nm/metrics.json', get_metrics),
                       url(r'^esgf-nm/registration.xml', get_reg_xml))

