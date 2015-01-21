from threading import Thread
from time import time

from httplib import HTTPConnection as Conn

def init_node_list():

    org_list = [ "aims1.llnl.gov" ]

    for n in range(1,4):

        org_list.append("greyworm"+ str(n) + ".llnl.gov")

    return org_list

node_list = init_node_list()

def get_node_list():
    return node_list




class RunningCheck(Thread):

    def __init__(self, nodename, fwdcheck, first, checkarr):
        super(RunningCheck, self).__init__()
        self.nodename = nodename
        self.fwdcheck = fwdcheck
        self.eltime = -1
        self.first = first
        self.checkarr = checkarr

    def run(self):

        ts = time()

        conn = Conn(self.nodename, 80, timeout=30)
    
        conn.request("GET", "/health-check-api/?from=" + self.nodename + "&forward=" + str(self.fwdcheck))
        
        resp = conn.getresponse()

        eltime = time() - ts
        
        checkarr.append(self.nodename + " " + str(eltime))

        if (first):
            if len(node_list) > len(checkarr) + 2:
                sleep(.01)
        
        


def do_checks(fwdcheck):

    tarr = []

    for n in get_node_list():


        if n != hostname:
                t = RunningCheck(n, True)
                t.start()
                tarr.append(t)

    
    if (fwdcheck):
    
        for tt in tarr:

            tt.join()
            print tt.hostname, tt.eltime
