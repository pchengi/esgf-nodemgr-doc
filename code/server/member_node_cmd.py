import sys, os

from httplib import HTTPConnection as Conn




cmd = sys.argv[1]

myname = os.uname()[1]


if cmd == "add":

    target = sys.argv[2]
    proj = sys.argv[3]
    
    stdby = sys.argv[4]

    conn = Conn(target, 80, timeout=30)

    try:
        conn.request("GET", "/esgf-nm-api?action=add_member&from=" + myname + "&project=" + proj + "&standby=" + stdby)
        resp = conn.get_response     
    except:
        print "Error in connection"

elif cmd ==  "remove":
    conf = sys.argv[2]

    import json

    f = open(conf)

    target = ""

    for entry in json.loads(f.read()):

        if "members" in entry:

            for

    conn = Conn(target, 80, timeout=30)

    try:
        conn.request("GET", "/esgf-nm-api?action=remove_member&from=" + myname )
        resp = conn.get_response     
    except:
        print "Error in connection"


    
    
