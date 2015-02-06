import json
import os

MAPFILE = ""



class NodeMap():

    def __init__(self):

        self.nodemap = json.loads(MAPFILE)
        self.myname = os.uname()[1]

        myid = -1
        for n in self.nodemap["supernodes"]:

            if n["hostname"] == self.myname:
                myid = n["id"]
        
        self.myid = myid
        

    def num_members(x):

        return len(x["members"])

    def get_supernode_list():

        sns = self.nodemap["supernodes"]

        return [row["hostname"] for row in sns]

    def get_member_nodes():

        mns = self.nodemap["membernodes"]

        for n in mns:

            if n["supernode"] == self.myid:
                
                return [row["hostname"] for row in mns["members"]


    def assign_node(node_name, project, standby=False):

        

        ref = self.nodemap["membernodeds"]
        
        fewest = min(ref, key=num_members))

        mnode_count = int(self.nodemap["total_membernodes"])
        snode_count = int(self.nodemap["total_supernodes"])
        
        mnode_count = mnode_count + 1

        new_node = {}
        new_node["id"] = str(nmode_count + snode_count)
        new_node["hostname"] = node_name
        new_node["standby"] = standby
        new_node["project"] = project
        fewest["members"].append(new_node)

        self.nodemap("total_membernodes") = mnode_count

        if fewest["supernode"] == self.myid:
            return True
        return False

    def write_back():

        outs = json.dumps(self.nodemap, sort_keys=True, indent=4, separators=(',', ': '))

        f = open(MAPFILE, "w")
        f.write(outs)
        f.close()
        

