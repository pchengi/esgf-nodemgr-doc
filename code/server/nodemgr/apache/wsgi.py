"""
This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os, sys

sys.path.insert(0, '/opt/nfs/ames4/esgf-node-manager/code/server/nodemgr')



os.environ["ESGF_NODEMGR_MAP"] = "/opt/nfs/ames4/esgf-nodemgr-doc/code/conf_examples/nm_2.map" 
os.environ["ESGF_NM_TASKS"] = "/esg/tasks"
os.environ["ESGF_NM_TIMESTAMP"] = "/esg/config/timestamp"
os.environ["ESGF_NM_PORT"]="6720"



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
