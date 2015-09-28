import sys, os

from httplib import HTTPConnection as Conn




cmd = sys.argv[1]

myname = os.uname()[1]

PORT = int(os.environ.get("ESGF_NM_PORT")

if cmd == "add":

    target = sys.argv[2]
    proj = sys.argv[3]
    
    stdby = sys.argv[4]

    conn = Conn(target, PORT, timeout=30)


    conn.request("GET", "/esgf-nm-api?action=add_member&from=" + myname + "&project=" + proj + "&standby=" + stdby)
    resp = conn.getresponse()
    conn.close()


elif cmd ==  "remove":
    conf = sys.argv[2]

    import json

    f = open(conf)

    target = ""

    targetnum = 0
    
    nodemap = json.loads(f.read())

    for entry in nodemap["membernodes"]:

        if "members" in entry:

            for mn in entry["members"]:
                if mn["hostname"] == myname:
                    targetnum = int(entry["supernode"])
                    break
        if targetnum > 0:
            for sn in nodemap["supernodes"]:
                if int(sn["id"]) == targetnum:
                    target = sn["hostname"]
                    break
            
            break
        

    if target == "":
        print "An error has occurred.  The supernode managing this node not found in the node map."
        exit

    conn = Conn(target, PORT, timeout=30)

    conn.request("GET", "/esgf-nm-api?action=remove_member&from=" + myname )
    resp = conn.getresponse()
    conn.close()
    


    
    
