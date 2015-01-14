from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.http import HttpResponse

def healthcheckack(request):

    return HttpResponse("OK")
    



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nodemgr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)
     url(r'^health-check-api/', healthcheckack, name=healthcheckack),)
