import json
import os


# this should be set by a global config
MAXREF = 20

class NodeMap():
    
    def __init__(self):
        self.filename = ""
        

    def load_map(self,MAPFILE):

        if (self.filename != ""):
            print "Initial map already loaded"
            return
        
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
        
        self.filename = MAPFILE
        
        

    def num_members(self,x):

        return len(x["members"])

    def get_supernode_list(self):

        return self.snidx.keys()

    def get_member_nodes(self):

        mns = self.nodemap["membernodes"]

        for n in mns:

            if n["supernode"] == self.myid:
                
                if "members" in n:
                    return [row["hostname"] for row in n["members"]]
                else:
                    return []

    def update_membernode_status(self, mn_hostname, status):

        mns = self.nodemap["membernodes"]

        for n in mns:

            if n["supernode"] == self.myid:
                for i in n["members"]:
                    if i["hostname"] == mn_hostname and i["health"] != status:
                        i["health"] = status
                        self.dirty = True

        
                        

    def assign_node(self, node_name, project, standby=False):

        

        ref = self.nodemap["membernodes"]

        mincount = MAXREF + 1

        for entry in ref:
            
            found = False

        

            if ( "members" in entry):
                members = entry["members"]
                count = len(members)
                for mn in members:
                    if mn["hostname"] == node_name:
                        if mn["standby"] != standby:
                            mn["standby"] = standby
                            self.dirty = True
                        found = True
                        if int(entry["supernode"]) == self.myid:
                            return True
                        return False
                        
                if count < mincount:
                    mincount = count
                    fewest = entry
            else:
                newlist = []
                entry["members"] = newlist
                fewest = entry
                break


#        fewest = min(ref, key=lambda x: len(x["members"]))



        mnode_count = int(self.nodemap["total_membernodes"])
        snode_count = int(self.nodemap["total_supernodes"])
        
        mnode_count = mnode_count + 1

        new_node = {}
        new_node["id"] = str(mnode_count + snode_count)
        new_node["hostname"] = node_name
        new_node["standby"] = standby
        new_node["project"] = project
        new_node["health"] = "unverified"
        fewest["members"].append(new_node)

        self.nodemap["total_membernodes"] = mnode_count

        self.dirty = True

        if fewest["supernode"] == self.myid:
            return True

        return False

    def remove_member(self, hostname):

        for entry in self.nodemap["membernodes"]:

            if entry["supernode"] == self.myid:
                
                memlist = entry["members"]
                for member in memlist:

                    if member["entry"] == hostname:

                        memlist.remove(member)
                        self.dirty = True
                        return True
                return False
                     

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
