# Offline script to add supernode entries to node manager json configuration node map file

import json, sys, os

if len(sys.argv) < 3:  
    print "need at least 2 <hostname> arguments"
    print "Example:"
    print sys.argv[0] + " node1.somedomain.org node2.other.gov node3.somewhere.edu ..."
    exit

filename = os.environ.get("ESGF_NODEMGR_MAP")

if filename is None or len(filename) == 0:
    print "Need to set variable ESGF_NODEMGR_MAP"
    exit


new_json = {}

supernodes = []

membernodes = []

links = []

i = 1


for nn in sys.argv[1:]:

    tmp_supernode = {}


    tmp_supernode["id"] = str(i)
    tmp_supernode["health"] = "new"
    tmp_supernode["hostname"] = nn

    supernodes.append(tmp_supernode)

    tmp_entry = {}
    tmp_entry["members"] = []
    tmp_entry["supernode"] = str(i)

    membernodes.append(tmp_entry)

    i = i + 1 
    


new_json["membernodes"] = membernodes
new_json["supernodes"] = supernodes

sn_count = len(supernodes)

new_json["total_supernodes"] = sn_count
new_json["total_membernodes"] = 0

for fr in range(1, sn_count):

    for tt in range(fr + 1, sn_count+1):

        new_link = {}
        
        new_link["from"] = str(fr)
        new_link["to"] = str(tt)
        new_link["status"] = "unverified"
        new_link["speed"] = 0

        links.append(new_link)


new_json["links"] = links

outf = open(filename, "w")

outs = json.dumps(new_json,  sort_keys=True, indent=4, separators=(',', ': '))
outf.write(outs)
outf.close()


    


