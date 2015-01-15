#!/usr/bin/env python
import os
import sys

from threading import Thread

from httplib import HTTPConnection as Conn

from time import time, sleep

INIT_CHECK = False



class RunningCheck(Thread):

    def __init__(self, nodename):
        super(RunningCheck, self).__init__()
        self.nodename = nodename
        

    def run(self):

        ts = time()

        conn = Conn(nodename + ".llnl.gov", 80, timeout=30)
    
        conn.request("GET", "/health-check-api/?from=" + nodename + "&forward=true")
        
        eltime = time() - time

        


def do_work():

    hostname = os.uname()[1]

    while True:

        sleep(30)
    
        
    
    


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nodemgr.settings")

    from django.core.management import execute_from_command_line

    
    if init_check:
        th = Thread(target = do_work())
        th.start()
        

    execute_from_command_line(sys.argv)
