import os, json

from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.http import HttpResponse #, QueryDict

from healthcheck import RunningCheck

from simplequeue import write_task
from nodemap import NodeMap
from api import nodemgrapi


#hostname = os.uname()[1]

#checkarr = []
#MAPFILE = "/export/ames4/node_mgr_map.json"

#nodemap_instance = NodeMap(MAPFILE)

def healthcheckreport(request):
    qd = request.GET

    outd = qd.copy()
    outd["action"] = "health_check_report"
    

    write_task(json.dumps(outd))

    return HttpResponse("")

def healthcheckack(request):

    qd = request.GET



    if ("forward" in qd and qd["forward"] == "True"):

        outd = qd.copy()

        outd["action"] = "health_check_fwd"
        write_task(json.dumps(outd))
        print "checking on others"        

    return HttpResponse("OK")
    


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nodemgr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)
                       url(r'^health-check-api/', healthcheckack, name=healthcheckack),
                       url(r'^health-check-rep', healthcheckreport, name=healthcheckreport),
                       url(r'^esgf-nm-api', nodemgrapi, name=nodemgrapi),)

