import json
import os



class NodeMap():
    
    def __init__(self):
        self.filename = ""
        

    def load_map(self,MAPFILE):

        if (self.filename != ""):
            print "Initial map already loaded"
            return
        
        self.filename = MAPFILE
        
        f = open(MAPFILE)
        
        self.nodemap = json.loads(f.read())
        f.close()
        self.myname = os.uname()[1]

        self.snidx = {}
        myid = -1
        for n in self.nodemap["supernodes"]:
            
            hostname = n["hostname"]
            self.snidx[hostname] = n["id"]
            
            if hostname == self.myname:
                myid = n["id"]
        
        if myid == -1:
            print "ERROR: node not in supernode list"
            exit (1)
        self.myid = myid
        self.dirty = False
        
        

    def num_members(self,x):

        return len(x["members"])

    def get_supernode_list(self):

        return self.snidx.keys()

    def get_member_nodes(self):

        mns = self.nodemap["membernodes"]

        for n in mns:

            if n["supernode"] == self.myid:
                
                return [row["hostname"] for row in mns["members"]]


    def update_membernode_status(self, mn_hostname, status):

        mns = self.nodemap["membernodes"]

        for n in mns:

            if n["supernode"] == self.myid:
                for i in n["members"]:
                    if i["hostname"] == nm_hostname and i["status"] != status:
                        i["status"] = status
                        self.dirty = True

        
                        

    def assign_node(self, node_name, project, standby=False):

        

        ref = self.nodemap["membernodeds"]
        
        fewest = min(ref, key=num_members)

        mnode_count = int(self.nodemap["total_membernodes"])
        snode_count = int(self.nodemap["total_supernodes"])
        
        mnode_count = mnode_count + 1

        new_node = {}
        new_node["id"] = str(nmode_count + snode_count)
        new_node["hostname"] = node_name
        new_node["standby"] = standby
        new_node["project"] = project
        fewest["members"].append(new_node)

        self.nodemap["total_membernodes"] = mnode_count

        self.dirty = True

        if fewest["supernode"] == self.myid:
            return True

        return False

    def write_back(self):

        # We only write if there are changes
        if self.dirty == False:
            return
        
        print ("updating the file")
        outs = json.dumps(self.nodemap, sort_keys=True, indent=4, separators=(',', ': '))

        f = open(self.filename, "w")
        f.write(outs)
        f.close()
        self.dirty = False
        


nodemap_instance = NodeMap()

def get_instance():
    return nodemap_instance
