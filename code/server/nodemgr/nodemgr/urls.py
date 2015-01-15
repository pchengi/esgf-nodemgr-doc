from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.http import HttpResponse


def init_node_list():

    org_list = [ "aims1" ]

    for n in range(1,9):

        org_list.append("greyworm"+ str(n))

    return org_list

node_list = init_node_list()


def healthcheckack(request):

    if request.

    return HttpResponse("OK")
    



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nodemgr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)
     url(r'^health-check-api/', healthcheckack, name=healthcheckack),)
