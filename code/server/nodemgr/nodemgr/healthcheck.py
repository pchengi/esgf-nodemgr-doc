from threading import Thread
from time import time, sleep

from nodemap import get_instance

from httplib import HTTPConnection as Conn

import os




# def init_node_list():

#     org_list = [ "aims1.llnl.gov" ]

#     for n in range(1,4):

#         org_list.append("greyworm"+ str(n) + ".llnl.gov")

#     return org_list

# node_list = init_node_list()

# def get_node_list():
#     return node_list


localhostname = os.uname()[1]

# MAPFILE = "/export/ames4/node_mgr_map.json"




class RunningCheck(Thread):

    def __init__(self, nodename, fwdcheck, first=False, checkarr=None, fromnode=""):
        super(RunningCheck, self).__init__()
        self.nodename = nodename
        self.fwdcheck = fwdcheck
        self.eltime = -1
        self.first = first
        self.checkarr = checkarr
        self.fromnode = fromnode


    def run(self):

        ts = time()
        print self.nodename

        conn = Conn(self.nodename, 80, timeout=30)


        eltime = -1
        error = ""
        try:
            conn.request("GET", "/health-check-api/?from=" + localhostname + "&forward=" + str(self.fwdcheck))
        
            resp = conn.getresponse()

            eltime = time() - ts
        except:
            error = "connectivity problem"

        self.eltime = eltime

        nodemap_instance = get_instance()
        node_list = nodemap_instance.get_supernode_list()

        if not self.fwdcheck:
            
            if not self.checkarr is None:
                self.checkarr.append(self.nodename + "=" + str(eltime))

            if (self.first):
                if len(node_list) > len(self.checkarr) + 2:
                    sleep(.01)
                conn = Conn(self.fromnode, 80, timeout=30)
                url = "/health-check-rep?from=" + localhostname

                for n in self.checkarr:
                    url = url + "&" + n
                conn.request("GET", url)
                resp = conn.getresponse()


# def do_checks(fwdcheck):

#     tarr = []

#     for n in nodemap_instance.get_supernode_list():


#         if n != hostname:
#                 t = RunningCheck(n, True)
#                 t.start()
#                 tarr.append(t)



#     if (fwdcheck):
    
#         for tt in tarr:

#             tt.join()
#             tt.hostname, tt.eltime
