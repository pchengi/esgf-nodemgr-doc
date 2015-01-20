import os

from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.http import HttpResponse #, QueryDict

from healthcheck import RunningCheck, get_node_list


hostname = os.uname()[1]

def healthcheckack(request):

    qd = request.GET
    
    
    if ("forward" in qd and qd["forward"] == "True"):
        
        fromnode = qd["from"]

        print "checking on others"

        tarr = []

# Refactor with manager.py block
        for n in get_node_list():
            
            if (n != hostname and  n != fromnode ):
                t = RunningCheck(n, False)
                t.start()
                tarr.append(t)



    return HttpResponse("OK")
    



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nodemgr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)
     url(r'^health-check-api/', healthcheckack, name=healthcheckack),)
